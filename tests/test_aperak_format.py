import json
import unittest

from ediel_parser.lib.EDIParser import EDIParser
from ediel_parser.lib.UNSegment import UNSegment
from tests.utils import get_tag


class TestEdielParser(unittest.TestCase):
    edi = (
        "UNA:+.? 'UNB+UNOC:3+91100:ZZ+92165:ZZ+230420:1534+E230420754641++23-DDQ-E66-S++1'"
        "UNH+1+UTILTS:D:02B:UN:E5SE1B'BGM+E66::260+E230420754642+9+AB'DTM+137:202304201434:203'"
        "DTM+735:?+0100:406'MKS+23+E02::260'NAD+DDQ'NAD+MR+92165:SVK:260'NAD+MS+91100:SVK:260'"
        "IDE+24+E230420754639'LOC+239+TES:SVK:260'LOC+172+735999888000013017::9'LIN+++8716867000030:::9'"
        "DTM+324:202303010000202304010000:719'DTM+597:202304010000:203'DTM+354:1:802'STS+7++E88::260'"
        "MEA+AAZ++KWH'CCI+++E12::260'CAV+E17::260'SEQ++1'RFF+AES:101'RFF+MG:M-0131'QTY+220:1486'"
        "DTM+597:202303010000:203'CCI+++E22::260'CAV+E27::260'SEQ++2'RFF+AES:101'QTY+220:3016'"
        "DTM+597:202304010000:203'CCI+++E22::260'CAV+E27::260'SEQ++3'QTY+136:42'IDE+24+E230420754640'"
        "LOC+239+TES:SVK:260'LOC+172+735999888000013024::9'LIN+++8716867000030:::9'"
        "DTM+324:202303010000202304010000:719'DTM+597:202303010000:203'DTM+354:1:802'STS+7++E88::260'"
        "MEA+AAZ++KWH'CCI+++E12::260'CAV+E17::260'SEQ++1'RFF+AES:101'RFF+MG:M-0132'QTY+220:16080'"
        "DTM+597:202303010000:203'CCI+++E22::260'CAV+E27::260'SEQ++2'RFF+AES:101'QTY+220:36054'"
        "DTM+597:202304010000:203'CCI+++E22::260'CAV+E27::260'SEQ++3'QTY+136:19974'UNT+61+1'UNZ+1+E230420754641'"
    )
    output_format = "edi"
    test_ediel = "99999"
    test_country = "Uzbekistan"

    def runTest(self):
        ediel_parser = EDIParser(self.edi,
                                 self.output_format,
                                 self.test_ediel,
                                 self.test_country)
        aperak = ediel_parser.create_aperak()[0]
        print(ediel_parser.toEdi(aperak).replace("'", "'\n"))

        unb = get_tag(aperak, "UNB")
        unt = get_tag(aperak, "UNT")
        unh = get_tag(aperak, "UNH")
        self.assertEqual(
            unb['interchange_sender']['sender_identification'].value,
            self.test_ediel
        )
        self.assertEqual(
            unb['interchange_recipient']['recipient_identification'].value,
            ediel_parser.segments['UNB']['interchange_sender']['sender_identification'].value
        )
        self.assertEqual(
            unb['application_reference'].value,
            ediel_parser.segments['UNB']['application_reference'].value
        )
        self.assertEqual(
            unh['message_reference_number'].value,
            unt['message_reference_number'].value
        )
