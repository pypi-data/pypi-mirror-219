import struct
import sys
from decimal import Decimal
from ctypes import *
import zipfile
import os
import subprocess
r=os.path.abspath(os.path.dirname(__file__))
rootpath= os.path.split(r)[0]
sys.path.append(rootpath)

from vcarhilclient.Enums import *
import collections.abc
from bitstring import BitArray

class can_detail():
    def __init__(self):
        self.dlc = 0
        self.rtr = 0
        self.fdf = 0
        self.brs = 0
        self.ef = 0
        self.dir = 0
        self.protocol_id = 0
        self.id = 0
        self.extend = 0
        self.data = b''

class kunyi_util():
    @staticmethod
    def get_signal_bytes_length(signal_type, item_count=1, struct_detail=None, **sub_struct_detail):
        type_dict = {"Int8": 1,
                     "Int16": 2,
                     "Int32": 4,
                     "Int64": 8,
                     "UInt8": 1,
                     "UInt16": 2,
                     "UInt32": 4,
                     "UInt64": 8,
                     "Float": 4,
                     "Double": 8,
                     "Bool": 1,
                     "ASCII": 512,
                     "UTF8": 512}

        if signal_type == "Struct":
            if struct_detail == None:
                raise Exception("No struct detail for counting the length")
            total_length = 0
            for member in struct_detail["Member"]:
                if member["Type"] == "Struct":
                    if member["RefStruct"] not in sub_struct_detail:
                        raise Exception("No sub struct detail for counting the length")
                    sub_length = kunyi_util.get_signal_bytes_length(member["Type"],
                                                                    member["ItemCount"],
                                                                    sub_struct_detail[member["RefStruct"]],
                                                                    **sub_struct_detail)
                    total_length = total_length + sub_length
                else:
                    sub_length = kunyi_util.get_signal_bytes_length(member["Type"], member["ItemCount"], None)
                    total_length = total_length + sub_length
            return total_length * item_count

        elif signal_type in type_dict:
            return type_dict[signal_type] * item_count

        else:
            raise Exception("Unsupport datatype pass in")

    @staticmethod
    def bytes_to_data(datatype, bytes_data, item_count=1, struct_detail=None, **sub_struct_detail):
        decode_charactor = {
            "Int8": "b",
            "Int16": "h",
            "Int32": "i",
            "Int64": "q",
            "UInt8": "B",
            "UInt16": "H",
            "UInt32": "I",
            "UInt64": "Q",
            "Float": "f",
            "Double": "d",
            "Bool": "?" }
        all_values = []
        fetch_idx = 0
        if datatype == "Struct":
            for i in range(item_count):
                value = {}
                for member in struct_detail["Member"]:
                    member_type = member["Type"]
                    if member_type == "Struct":
                        if member["RefStruct"] not in sub_struct_detail:
                            raise Exception("No sub struct detail for counting the bytes")
                        member_byte_length = kunyi_util.get_signal_bytes_length(member_type,
                                                                                member["ItemCount"],
                                                                                sub_struct_detail[member["RefStruct"]],
                                                                                **sub_struct_detail
                                                                                )
                        member_bytes = bytes_data[fetch_idx, fetch_idx+member_byte_length]
                        value[member["Name"]] = kunyi_util.bytes_to_data(member_type, member_bytes,
                                                                         member["ItemCount"],
                                                                         sub_struct_detail[member["RefStruct"]],
                                                                        **sub_struct_detail)
                        fetch_idx = fetch_idx + member_byte_length
                    else:
                        member_byte_length = kunyi_util.get_signal_bytes_length(member_type,
                                                                                member["ItemCount"], None)
                        member_bytes = bytes_data[fetch_idx: fetch_idx + member_byte_length]
                        value[member["Name"]] = kunyi_util.bytes_to_data(member_type, member_bytes,
                                                                         member["ItemCount"], None)
                        fetch_idx = fetch_idx + member_byte_length
                all_values.append(value)
            if item_count == 1:
                return all_values[0]
            return all_values


        else:
            single_length = kunyi_util.get_signal_bytes_length(datatype, 1, None)

            for i in range(item_count):
                bytes_sub = bytes_data[i*single_length:(i+1)*single_length]
                if datatype in decode_charactor:
                    value = struct.unpack(decode_charactor[datatype],
                                          bytes_sub)[0]
                elif datatype == "ASCII":
                    value = bytes_sub.decode("ascii").strip('\x00')
                elif datatype == "UTF8":
                    value = bytes_sub.decode("utf-8").strip('\x00')

                all_values.append(value)
            if item_count == 1:
                return all_values[0]
            return all_values


    @staticmethod
    def bytes_array_to_data_array(datatype, bytes_data, item_count):
        item_data = []
        move_steps = kunyi_util.get_signal_bytes_length(datatype)
        loop_count = min(len(bytes_data)/move_steps, item_count)


        start_idx = 0
        for i in range(int(loop_count)):
            temp_array = bytes_data[start_idx: start_idx+move_steps]
            start_idx = start_idx+move_steps
            value = kunyi_util.bytes_to_data(datatype, temp_array, 1)
            item_data.append(value)
        return item_data


    @staticmethod
    def data_to_bytes(datatype, data_value, item_count=1, struct_detail=None, bit_order=None, **sub_struct_detail):
        bytes_result = b''
        decode_charactor = {
            "Int8": "b",
            "Int16": "h",
            "Int32": "i",
            "Int64": "q",
            "UInt8": "B",
            "UInt16": "H",
            "UInt32": "I",
            "UInt64": "Q",
            "Float": "f",
            "Double": "d",
            "Bool": "?"}


        if datatype == "Struct":
            if type(data_value) != dict:
                raise Exception("Data value is not match the data type")
            for member in struct_detail["Member"]:
                member_value = data_value[member["Name"]]
                member_type = member["Type"]
                if member_type == "Struct":
                    if member["RefStruct"] not in sub_struct_detail:
                        raise Exception("No sub struct detail for counting the bytes")
                    if member["ItemCount"] > 1:
                        if type(member_value) != list:
                            raise Exception("Data value is not enough for the array type")
                        for mi in range(member["ItemCount"]):
                            bytes_result = bytes_result + kunyi_util.data_to_bytes(member_type, member_value[mi],
                                                                               1,
                                                                               sub_struct_detail[member["RefStruct"]],
                                                                               **sub_struct_detail)
                    else:
                        bytes_result = bytes_result + kunyi_util.data_to_bytes(member_type, member_value,
                                                                               1,
                                                                               sub_struct_detail[member["RefStruct"]],
                                                                               **sub_struct_detail)
                else:
                    if member["ItemCount"] > 1:
                        if type(member_value) != list:
                            raise Exception("Data value is not enough for the array type")
                        for mi in range(member["ItemCount"]):
                            bytes_result = bytes_result + kunyi_util.data_to_bytes(member_type, member_value[mi],
                                                                               1, None)
                    else:
                        bytes_result = bytes_result + kunyi_util.data_to_bytes(member_type, member_value,
                                                                               1, None)
        else:
            if item_count > 1:
                if type(data_value) != list:
                    raise Exception("Data value is not enough for the array type")
                for mi in range(item_count):
                    if datatype in decode_charactor:
                        bytes_result = bytes_result + struct.pack(decode_charactor[datatype], data_value[mi])
                    elif datatype == "ASCII":
                        bytes_result = bytes_result + data_value[mi].encode("ascii")
                        break
                    elif datatype == "UTF8":
                        bytes_result = bytes_result + data_value[mi].encode("utf-8")
                        break
                    else:
                        raise Exception("Unsupportted type for counting the bytes")
            else:
                value = data_value
                if datatype in decode_charactor:
                    ff_str = decode_charactor[datatype]
                    if bit_order != None:
                        format_str = bit_order + decode_charactor[datatype]
                    bytes_result = bytes_result + struct.pack(ff_str, value)
                elif datatype == "ASCII":
                    bytes_result = bytes_result + value.encode("ascii")
                elif datatype == "UTF8":
                    bytes_result = bytes_result + value.encode("utf-8")
                else:
                    raise Exception("Unsupportted type for counting the bytes")

        return bytes_result

    @staticmethod
    def msg_to_can_detail(data):
        result = can_detail()
        flag_bytes = kunyi_util.data_to_bytes("UInt32", data["flags"], 1)
        aaa = str(flag_bytes.hex())
        first_byte = BitArray('0x'+ aaa[0:2])
        dlc_bit = '0000' + first_byte.b[::-1][0:4][::-1]
        result.dlc = int(dlc_bit, base=2)
        third_byte = BitArray('0x'+ aaa[4:6])
        rtr_bit = '0000000' + third_byte.b[::-1][0:1]
        fdf_bit = '0000000' + third_byte.b[::-1][1:2]
        brs_bit = '0000000' + third_byte.b[::-1][2:3]
        ef_bit = '0000000' + third_byte.b[::-1][5:6]
        dir_bit = '0000000' + third_byte.b[::-1][-1]
        last_byte = BitArray('0x' + aaa[-2:])
        pro_id_bit = '0000' + last_byte.b[::-1][-4:]
        result.rtr = int(rtr_bit, base=2)
        result.fdf = int(fdf_bit, base=2)
        result.brs = int(brs_bit, base=2)
        result.ef = int(ef_bit, base=2)
        result.dir = int(dir_bit, base=2)
        result.protocol_id = int(pro_id_bit, base=2)

        id_bytes = kunyi_util.data_to_bytes("UInt32", data["id"], 1, bit_order='>')
        all_bytes = BitArray('0x'+ str(id_bytes.hex()))
        id_bit = '000'+ all_bytes.b[-29:]
        result.id = int(id_bit, base=2)
        extend_bit = '0000000' + all_bytes.b[-32:31][-1]
        result.extend = int(extend_bit, base=2)
        data_sub = data['data'][0:result.dlc]
        data_bytes = b''
        for dd in data_sub:
            data_bytes = data_bytes + kunyi_util.data_to_bytes("UInt8", dd, 1, struct=None, bit_order=None)

        result.data = data_bytes
        return result


    @staticmethod
    def file_compress(root_path, out_zip_file):
        import shutil
        shutil.make_archive(out_zip_file, 'zip', root_path)
        return out_zip_file + ".zip"

    @staticmethod
    def file_uncompress(filPath, targetPath):
        import shutil
        shutil.unpack_archive(filPath,targetPath)
        return targetPath

    @staticmethod
    def mrt_datatype_to_hil_datatype(mrt_datatype):
        all_dt = {
            "MRT_DATA_TYPE_UINT8": "UInt8",
            "MRT_DATA_TYPE_UINT16": "UInt16",
            "MRT_DATA_TYPE_UINT32": "UInt32",
            "MRT_DATA_TYPE_UINT64": "UInt64",
            "MRT_DATA_TYPE_INT8": "Int8",
            "MRT_DATA_TYPE_INT16": "Int16",
            "MRT_DATA_TYPE_INT32": "Int32",
            "MRT_DATA_TYPE_INT64": "Int64",
            "MRT_DATA_TYPE_FLOAT32": "Float",
            "MRT_DATA_TYPE_FLOAT64": "Double",
            "MRT_DATA_TYPE_STRUCT": "Struct"
        }

    @staticmethod
    def string_to_mrt_signal_type(str_signal_type):
        type_dict = {
            "InputPorts": mrt_port_type_t.MRT_INPUT_PORT,
            "OutputPorts": mrt_port_type_t.MRT_OUTPUT_PORT,
            "Measurements": mrt_port_type_t.MRT_MEASUREMENT

        }
        if str_signal_type not in type_dict:
            return -1
        else:
            return type_dict[str_signal_type]



    @staticmethod
    def get_funinx_by_xy(xidx, yidx, xlength):
        return yidx * xlength + xidx



class decimal_data(Union):
    _fields_ = [("a", c_double),
                ("b", c_ubyte * 8)]