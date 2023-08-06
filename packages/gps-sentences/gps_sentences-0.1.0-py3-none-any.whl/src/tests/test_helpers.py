from src.helpers.helpers import NMEASerialReader, NMEASerialDecode


def test_lat_conversion_1():
    lat = NMEASerialDecode
    assert lat.lat_conversion("0") == 0


def test_lat_conversion_2():
    assert NMEASerialDecode.lat_conversion("2617.17091") == 26.286182


def test_lat_conversion_3():
    assert NMEASerialDecode.lat_conversion("2617.17184") == 26.286197


def test_lat_conversion_4():
    assert NMEASerialDecode.lat_conversion("2617.17079") == 26.28618


def test_lat_conversion_5():
    assert NMEASerialDecode.lat_conversion("2617.17077") == 26.286179


def test_long_conversion_1():
    long = NMEASerialDecode
    assert long.long_conversion("0") == 0


def test_long_conversion_2():
    assert NMEASerialDecode.long_conversion("08017.50233") == 80.291706


def test_long_conversion_3():
    assert NMEASerialDecode.long_conversion("08017.50047") == 80.291674


def test_long_conversion_4():
    assert NMEASerialDecode.long_conversion("08017.50166") == 80.291694


def test_long_conversion_5():
    assert NMEASerialDecode.long_conversion("08017.54532") == 80.292422


def test_slice_1():
    slice = NMEASerialDecode
    assert slice.slice_time("000000.00") == "00:00:00"


def test_slice_2():
    assert NMEASerialDecode.slice_time("000001.00") == "00:00:01"


def test_slice_3():
    assert NMEASerialDecode.slice_time("000002.00") == "00:00:02"


def test_slice_4():
    assert NMEASerialDecode.slice_time("000003.00") == "00:00:03"


def test_slice_5():
    assert NMEASerialDecode.slice_time("000004.00") == "00:00:04"


def test_change_to_list_1():
    assert NMEASerialDecode.change_to_list("08,23,41,23412,434,432") == [
        "08", "23", "41", "23412", "434", "432"]


def test_change_to_list_2():
    assert NMEASerialDecode.change_to_list("132,3213,3,643,634,342") == [
        "132", "3213", "3", "643", "634", "342"]


def test_change_to_list_3():
    assert NMEASerialDecode.change_to_list("1,2,3,4,5,6") == [
        "1", "2", "3", "4", "5", "6"]


def test_change_to_list_4():
    assert NMEASerialDecode.change_to_list("1,7,2,4,7,2,7,94,3") == [
        "1", "7", "2", "4", "7", "2", "7", "94", "3"]


def test_change_to_list_5():
    assert NMEASerialDecode.change_to_list("432423,213,5324,123,4,642,65743412,231,432") == [
        "432423", "213", "5324", "123", "4", "642", "65743412", "231", "432"]


def test_decode_alt_1():
    assert NMEASerialDecode.decode_alt(['$GPGGA', '185535.00', '2617.17985', 'N', '08017.49640',
                                       'W', '1', '08', '1.25', '17.4', 'M', '-27.0', 'M', '', '*54']) == "17.4"


def test_decode_alt_2():
    assert NMEASerialDecode.decode_alt(['$GPGGA', '185949.00', '2617.17170', 'N', '08017.50155',
                                       'W', '1', '08', '1.25', '6.3', 'M', '-27.0', 'M', '', '*6D']) == "6.3"


def test_decode_alt_3():
    assert NMEASerialDecode.decode_alt(['$GPGGA', '185949.00', '2617.17170', 'N', '08017.50155',
                                       'W', '1', '08', '1.25', '4213.3', 'M', '-27.0', 'M', '', '*6D']) == "4213.3"


def test_decode_alt_4():
    assert NMEASerialDecode.decode_alt(['$GPGGA', '185949.00', '2617.17170', 'N', '08017.50155',
                                       'W', '1', '08', '1.25', '564', 'M', '-27.0', 'M', '', '*6D']) == "564"


def test_decode_alt_5():
    assert NMEASerialDecode.decode_alt(['$GPGGA', '185949.00', '2617.17170', 'N', '08017.50155',
                                       'W', '1', '08', '1.25', '0.0', 'M', '-27.0', 'M', '', '*6D']) == "0.0"
