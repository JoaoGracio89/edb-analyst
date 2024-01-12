from datetime import *
import struct
import binascii

global_page_size = 8192
global_page_data_size = 8128

def check_sum(data):
    print("check_sum")
    print(data.hex())

def signature(data):
    print("signature")
    print(data.hex())

def file_format_version(data):
    print("file_format_version")
    print(data.hex())

def file_type(data):
    print("file_type")
    print(data.hex())

def database_time(data):
    unknown_empty_value(data)

def database_signature(data):
    print("database_signature")
    if(data == 0):
        print("HIERARCHICAL DATABASE")
    else:
        print("STREAMING FILE STREAMED DATABASE")

def database_state(data):
    print("database_state")
    data_int = int.from_bytes(data, byteorder='little')
    if(data_int == 1):
        print("DATABASE JUST CREATED")
    elif(data_int == 2):
        print("DATABASE DIRTY SHUTDOWN")
    elif(data_int == 3):
        print("DATABASE CLEAN STATE")
    elif(data_int == 4):
        print("DATABASE IS BEING UPGRADED")
    elif(data_int == 5):
        print("DATABASE FORCE DETACH (INTERNAL)")

def consistent_position(data):
    log_position(data, "consistent_position")

def consistent_date_and_time(data):
    log_backup_log_time(data, "consistent_date_and_time")

def attach_date_and_time(data):
    log_backup_log_time(data, "attach_date_and_time")



'''
Backup log time (8.3) 
'''
def log_backup_log_time(data, function_name=None):
    months = int.from_bytes(retrieve_bytes_from_range(data, 4, 5), byteorder='little')
    years = int.from_bytes(retrieve_bytes_from_range(data, 5, 6), byteorder='little')
    time_delta = timedelta(seconds=int.from_bytes(retrieve_bytes_from_range(data, 0, 1), byteorder='little'),
                           minutes=int.from_bytes(retrieve_bytes_from_range(data, 1, 2), byteorder='little'),
                           hours=int.from_bytes(retrieve_bytes_from_range(data, 2, 3), byteorder='little'),
                           days=int.from_bytes(retrieve_bytes_from_range(data, 3, 4), byteorder='little') + years * 365 + months * 30)

    base_time_delta = datetime(1900, 1, 1)

    final_time_delta = base_time_delta + time_delta

    if function_name is None:
        print("backup_log_time: {0}".format(final_time_delta))
    else:
        print_output = ("backup_log_time " + function_name + ": {0}".format(final_time_delta))
        print(print_output)

    return final_time_delta


def log_position(data, function_name=None):
    if function_name is None:
        print("consistent_position_block: {0}".format(retrieve_bytes_from_range(data, 0, 2).hex()))
        print("consistent_position_sector: {0}".format(retrieve_bytes_from_range(data, 2, 4).hex()))
        print("consistent_position_generation: {0}".format(retrieve_bytes_from_range(data, 4, 8).hex()))
    else:
        print_output = ("consistent_position_block " + function_name + ": {0}".format(retrieve_bytes_from_range(data, 0, 2).hex()))
        print(print_output)
        print_output = ("consistent_position_sector " + function_name + ": {0}".format(retrieve_bytes_from_range(data, 2, 4).hex()))
        print(print_output)
        print_output = ("consistent_position_generation " + function_name + ": {0}".format(retrieve_bytes_from_range(data, 4, 8).hex()))
        print(print_output)


def unknown_empty_value(data, function_name=None):
    if function_name is None:
        print("unknown_empty_value")
        print(data.hex())
    else:
        print_output = (function_name + "unknown_empty_value")
        print(print_output)
        print(data.hex())

def attach_position(data):
    log_position(data, "attach_position")

def detach_date_and_time(data):
    log_backup_log_time(data, "detach_date_and_time")

def detach_position(data):
    log_position(data, "detach_position")


def hex_to_ascii(data):
    try:
        # Decode the hex string to bytes
        byte_data = binascii.unhexlify(data)

        # Convert bytes to ASCII
        ascii_string = byte_data.decode('ascii')

        return ascii_string
    except binascii.Error as e:
        print(f"Error decoding hex string: {e}")
        return None

def netbios_ascii_representation(data, function_name=None):
    if function_name is None:
        print("netbios_ascii_representation")
        hex_to_ascii(data.hex())
    else:
        print_output = (function_name + " netbios_ascii_representation")
        ascii_representation = hex_to_ascii(data.hex())
        if ascii_representation is not None:
            print(print_output)
            print(ascii_representation)
        else:
            print("Error decoding hex string")

def database_signature(data):
    print("database_signature randomly assigned number {0}".format(int(retrieve_bytes_from_range(data, 0, 4).hex(), 16)))
    log_backup_log_time(retrieve_bytes_from_range(data, 4, 8), "database_signature")
    netbios_ascii_representation(retrieve_bytes_from_range(data, 8, 12), "database_signature")

def log_signature(data):
    database_signature(data)


def backup_information(data, function_name=None):
    if function_name is None:
        print_output = "backup_information"
    else:
        print_output = (function_name + " backup_information")

    log_position(retrieve_bytes_from_range(data, 0, 8), "previous_full_backup")
    log_backup_log_time(retrieve_bytes_from_range(data, 8, 16), "previous_full_backup")
    print(print_output + ": {0}".format(int(retrieve_bytes_from_range(data, 16, 20).hex()), 16))
    print(print_output + ": {0}".format(int(retrieve_bytes_from_range(data, 20, 24).hex()), 16))


def previous_full_backup(data):
    backup_information(data, "previous_full_backup")

def previous_incremental_backup(data):
    backup_information(data, "previous_incremental_backup")

def current_full_backup(data):
    backup_information(data, "current_full_backup")

def shadowing_disbled(data):
    unknown_empty_value(data, "shadowing_disbled")


def last_object_indentifier(data):
    unknown_empty_value(data, "last_object_indentifier")


def major_version(data):
    print("major_version")
    print(int.from_bytes(data, byteorder='little'))

def minor_version(data):
    print("minor_version")
    print(int.from_bytes(data, byteorder='little'))


def build_number(data):
    print("build_number")
    print(int.from_bytes(data, byteorder='little'))


def service_pack_number(data):
    print("service_pack_number")
    print(int.from_bytes(data, byteorder='little'))


def file_format_revision(data):
    print("file_format_revision")
    print(int.from_bytes(data, byteorder='little'))


def page_size(data):
    print("page_size")
    global global_page_size
    global_page_size = int.from_bytes(data, byteorder='little')
    print(global_page_size)


def repair_count(data):
    print("repair_count")
    print(int.from_bytes(data, byteorder='little'))


def repair_date_and_time(data):
    log_backup_log_time(data, "repair_date_and_time")


def scrub_database_date_and_time(data):
    database_signature(data)


def scrub_log_date_and_time(data):
    log_backup_log_time(data, "scrub_log_date_and_time")

def required_log(data):
    print("required_log")
    print(int.from_bytes(data, byteorder='little'))

def upgrade_exchange(data):
    unknown_empty_value(data, "upgrade_exchange")


def upgrade_free_pages(data):
    print("upgrade_free_pages")
    print(int.from_bytes(data, byteorder='little'))


def upgrade_space_map_pages(data):
    print("upgrade_space_map_pages")
    print(int.from_bytes(data, byteorder='little'))


def current_shadow_copy_backup(data):
    backup_information(data, "current_shadow_copy_backup")


def creation_file_format_version(data):
    print("creation_file_format_version")
    print(int.from_bytes(data, byteorder='little'))


def creation_file_format_revision(data):
    print("creation_file_format_revision")
    print(int.from_bytes(data, byteorder='little'))


def old_repair_count(data):
    print("old_repair_count")
    print(int.from_bytes(data, byteorder='little'))


def ecc_fix_success_count(data):
    print("ecc_fix_success_count")
    print(int.from_bytes(data, byteorder='little'))


def last_ecc_fix_success_date_and_time(data):
    log_backup_log_time(data, "last_ecc_fix_success_date_and_time")


def old_ecc_fix_success_count(data):
    print("old_ecc_fix_success_count")
    print(int.from_bytes(data, byteorder='little'))


def ecc_fix_error_count(data):
    print("ecc_fix_error_count")
    print(int.from_bytes(data, byteorder='little'))


def last_ecc_fix_error_date_and_time(data):
    log_backup_log_time(data, "last_ecc_fix_error_date_and_time")


def old_ecc_fix_error_count(data):
    print("old_ecc_fix_error_count")
    print(int.from_bytes(data, byteorder='little'))


def bad_check_sum_error_count(data):
    print("bad_check_sum_error_count")
    print(int.from_bytes(data, byteorder='little'))


def last_bad_check_sum_error_date_and_time(data):
    log_backup_log_time(data, "last_bad_check_sum_error_date_and_time")


def old_bad_check_sum_error_count(data):
    print("old_bad_check_sum_error_count")
    print(int.from_bytes(data, byteorder='little'))


def commited_log(data):
    unknown_empty_value(data, "commited_log")


def previous_shadow_copy_backup(data):
    backup_information(data, "previous_shadow_copy_backup")


def previous_differential_backup(data):
    backup_information(data, "previous_differential_backup")


def nls_major_version(data):
    unknown_empty_value(data, "nls_major_version")


def nls_minor_version(data):
    unknown_empty_value(data, "nls_minor_version")


byte_range_to_trigger = [
    (0, 4, check_sum),
    (4, 8, signature),
    (8, 12, file_format_version),
    (12, 16, file_type),
    (16, 24, database_time),
    (24, 52, database_signature),
    (52, 56, database_state),
    (56, 64, consistent_position),
    (64, 72, consistent_date_and_time),
    (72, 80, attach_date_and_time),
    (80, 88, attach_position),
    (88, 96, detach_date_and_time),
    (96, 104, detach_position),
    (104, 132, log_signature),
    (132, 136, unknown_empty_value),
    (136, 160, previous_full_backup),
    (160, 184, previous_incremental_backup),
    (184, 208, current_full_backup),
    (208, 212, shadowing_disbled),
    (212, 216, last_object_indentifier),
    (216, 220, major_version),
    (220, 224, minor_version),
    (224, 228, build_number),
    (228, 232, service_pack_number),
    (232, 236, file_format_version),
    (236, 240, page_size),
    (240, 244, repair_count),
    (244, 252, repair_date_and_time),
    (252, 280, unknown_empty_value),
    (280, 288, scrub_database_date_and_time),
    (288, 296, scrub_log_date_and_time),
    (296, 304, required_log),
    (304, 308, upgrade_exchange),
    (308, 312, upgrade_free_pages),
    (312, 316, upgrade_space_map_pages),
    (316, 340, current_shadow_copy_backup),
    (340, 344, creation_file_format_version),
    (344, 348, creation_file_format_revision),
    (348, 364, unknown_empty_value),
    (364, 368, old_repair_count),
    (368, 372, ecc_fix_success_count),
    (372, 380, last_ecc_fix_success_date_and_time),
    (380, 384, old_ecc_fix_success_count),
    (384, 388, ecc_fix_error_count),
    (388, 396, last_ecc_fix_error_date_and_time),
    (396, 400, old_ecc_fix_error_count),
    (400, 404, bad_check_sum_error_count),
    (404, 412, last_bad_check_sum_error_date_and_time),
    (412, 416, old_bad_check_sum_error_count),
    (416, 420, commited_log),
    (420, 444, previous_shadow_copy_backup),
    (444, 468, previous_differential_backup),
    (468, 508, unknown_empty_value),
    (508, 512, nls_major_version),
    (512, 516, nls_minor_version),
    (516, 664, unknown_empty_value),
    (664, 668, unknown_empty_value),
]

def previous_page_number(data):
    print("previous_page_number")
    print(int.from_bytes(data, byteorder='little'))

def next_page_number(data):
    print("next_page_number")
    print(int.from_bytes(data, byteorder='little'))

def father_data_page_number(data):
    print("father_data_page_number")
    print(int.from_bytes(data, byteorder='little'))

def available_data_size(data):
    print("available_data_size")
    global global_page_data_size
    global_page_data_size = int.from_bytes(data, byteorder='little')
    print(global_page_data_size)


def available_uncommitted_data_size(data):
    print("available_uncommitted_data_size")
    print(int.from_bytes(data, byteorder='little'))

def first_available_data_offset(data):
    print("first_available_data_offset")
    print(int.from_bytes(data, byteorder='little'))

def first_available_page_tag(data):
    print("first_available_page_tag")
    print(int.from_bytes(data, byteorder='little'))

def page_flags(data):
    print("page_flags"+data.hex())
    if(data.hex() == '00000001'):
        print("page_flags the page is root page")
    elif(data.hex() == '00000002'):
        print("page_flags the page is leaf page")
    elif(data.hex() == '00000003'):
        print("page_flags the page is parent page")
    elif(data.hex() == '00000008'):
        print("page_flags the page is empty page")
    elif(data.hex() == '00000010'):
        print("page_flags the page is unknown status page")
    elif(data.hex() == '00000020'):
        print("page_flags the page is space tree page")
    elif(data.hex() == '00000040'):
        print("page_flags the page is index page")
    elif(data.hex() == '00000080'):
        print("page_flags the page is long value page")
    elif(data.hex() == '00000100'):
        print("page_flags the page is unknown status page")
    elif(data.hex() == '00000200'):
        print("page_flags the page is unknown status page")
    elif(data.hex() == '00000400'):
        print("page_flags the page is unknown status page")
    elif(data.hex() == '00000800'):
        print("page_flags the page is unknown status page")
    elif(data.hex() == '00001000'):
        print("page_flags the page is unknown status page")
    elif(data.hex() == '00002000'):
        print("page_flags the page is record format / checksum format page")
    elif(data.hex() == '00004000'):
        print("page_flags the page is scrubed was zero-ed status page")
    elif(data.hex() == '00008000'):
        print("page_flags the page is unknown status page")

def extended_check_sum(data):
    print("extended_check_sum")
    print(data.hex())

def extended_check_sum_1(data):
    print("extended_check_sum_1")
    print(data.hex())

def extended_check_sum_2(data):
    print("extended_check_sum_2")
    print(data.hex())


def extended_check_sum_3(data):
    print("extended_check_sum_3")
    print(data.hex())

def page_number(data):
    print("page_number")
    print(int.from_bytes(data, byteorder='little'))

byte_range_to_trigger_page = [
    (0, 8, check_sum),
    (8, 16, database_time),
    (16, 20, previous_page_number),
    (20, 24, next_page_number),
    (24, 28, father_data_page_number),
    (28, 30, available_data_size),
    (30, 32, available_uncommitted_data_size),
    (32, 34, first_available_data_offset),
    (34, 36, first_available_page_tag),
    (36, 40, page_flags),
    (40, 48, extended_check_sum_1),
    (48, 56, extended_check_sum_2),
    (56, 64, extended_check_sum_3),
    (64, 72, page_number),
    (72, 80, unknown_empty_value),
]


def retrieve_bytes_from_range(data, start_bye, end_byte):
    return data[start_bye:end_byte]


def read_bytes_from_range(file_path, byte_range_list):
    with open(file_path, 'rb') as file:
        for start_byte, end_byte, function in byte_range_list:
            # Move the file cursor to the starting byte position
            file.seek(start_byte)

            # Read the specified range of bytes
            data = file.read(end_byte - start_byte)

            function(data)

            if(end_byte == 668):
                break


def read_bytes_from_page(file_path, page_byte_beginning, byte_range_list):
    with open(file_path, 'rb') as file:
        for start_byte, end_byte, function in byte_range_list:
            # Move the file cursor to the starting byte position
            file.seek(page_byte_beginning + start_byte)

            # Read the specified range of bytes
            data = file.read(end_byte - start_byte)

            function(data)

            if(end_byte == 80):
                break

def main():
    # Example: Read bytes 10 to 20 from a binary file
    file_path = "..\\Windows.edb"

    read_bytes_from_range(file_path, byte_range_to_trigger)
    print("================== HEADER END ==================")
    print("global_page_size: {0}".format(global_page_size))
    page_zero_offset = (2 * global_page_size) + global_page_size
    print("page_zero_offset: {0}".format(page_zero_offset))
    read_bytes_from_page(file_path, page_zero_offset, byte_range_to_trigger_page)
    page_data_offset = 80 + page_zero_offset + 16

if __name__ == "__main__":
    main()