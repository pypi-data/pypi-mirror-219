# ******************************************************************************
# Copyright (c) 2019 Analog Devices, Inc.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
# - Modified versions of the software must be conspicuously marked as such.
# - This software is licensed solely and exclusively for use with
#  processors/products manufactured by or for Analog Devices, Inc.
# - This software may not be combined or merged with other code in any manner
#  that would cause the software to become subject to terms and conditions
#  which differ from those listed here.
# - Neither the name of Analog Devices, Inc. nor the names of its contributors
#  may be used to endorse or promote products derived from this software
#  without specific prior written permission.
# - The use of this software may or may not infringe the patent rights of one
#  or more patent holders.  This license does not release you from the
#  requirement that you obtain separate licenses from these patent holders to
#  use this software.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# NONINFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, DAMAGES ARISING OUT OF
# CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ******************************************************************************

from unittest import TestCase

from . import common_test
from ..adi_study_watch import SDK


def callback(data):
    print(data)


class TestADPDApplication(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.application = SDK("COM4").get_adpd_application()
        cls.application.set_callback(callback, stream=cls.application.STREAM_ADPD6)
        cls.application.set_timeout(20)

    def test_calibrate_clock(self):
        x = self.application.calibrate_clock(self.application.CLOCK_1M_AND_32M)
        assert (x["payload"]["clock_id"] == self.application.CLOCK_1M_AND_32M)

    def test_create_device_configuration(self):
        x = self.application.create_device_configuration(
            [[self.application.SLOT_A, self.application.APP_ECG],
             [self.application.SLOT_B, self.application.APP_ADPD_GREEN]])
        assert (x["payload"]["size"] == 2)
        assert (x["payload"]["data"] == [[self.application.SLOT_A, self.application.APP_ECG],
                                         [self.application.SLOT_B, self.application.APP_ADPD_GREEN]])

    def test_device_configuration(self):
        x = self.application.get_device_configuration()
        assert (type(x[0]["payload"]["size"]) == int)
        assert (type(x[0]["payload"]["data"]) == list)

    def test_device_configuration_block(self):
        x = self.application.write_device_configuration_block([[0x20, 0x2222], [0x123, 0x0034]])
        assert (x[0]["payload"]["size"] == 0)
        x = self.application.read_device_configuration_block()
        assert (x[0]["payload"]["data"] == [['0x20', '0x2222'], ['0x123', '0x34']])
        x = self.application.delete_device_configuration_block()
        assert (x["payload"]["size"] == 0)

    def test_load_configuration(self):
        x = self.application.load_configuration(self.application.DEVICE_GREEN)
        assert (x["payload"]["device_id"] == self.application.DEVICE_GREEN)

    def test_enable_disable_slot(self):
        x = self.application.disable_slot(self.application.SLOT_A)
        assert (x["payload"]["slot_num"] == self.application.SLOT_A)
        assert (x["payload"]["slot_enabled"] is False)
        x = self.application.enable_slot(self.application.SLOT_A)
        assert (x["payload"]["slot_num"] == self.application.SLOT_A)
        assert (x["payload"]["slot_enabled"] is True)

    def test_get_communication_mode(self):
        x = self.application.get_communication_mode()
        assert (type(x["payload"]["com_mode"]) == int)

    def test_decimation_factor(self):
        x = self.application.get_decimation_factor(self.application.STREAM_ADPD6)
        assert (type(x["payload"]["decimation_factor"]) == int)
        x = self.application.set_decimation_factor(2)
        assert (x["payload"]["decimation_factor"] == 2)

    def test_slot(self):
        x = self.application.get_slot(self.application.SLOT_F)
        assert (x["payload"]["slot_num"] == self.application.SLOT_F)
        x = self.application.set_slot(self.application.SLOT_F, True, 3, 3)
        assert (x["payload"]["slot_num"] == self.application.SLOT_F)
        assert (x["payload"]["slot_enabled"] is True)
        assert (type(x["payload"]["slot_format"]) == int)
        assert (type(x["payload"]["channel_num"]) == int)

    def test_get_sensor_status(self):
        x = self.application.get_sensor_status()
        assert (type(x["payload"]["num_subscribers"]) == int)
        assert (type(x["payload"]["num_start_registered"]) == int)

    def test_get_slot_status(self):
        x = self.application.get_slot_status(self.application.SLOT_A)
        assert (x["payload"]["slot_enabled"] is True)

    def test_get_version(self):
        x = self.application.get_version()
        assert (type(x["payload"]["major_version"]) == int)

    def test_pause_resume(self):
        x = self.application.pause()
        assert (x["payload"]["device_id"] == self.application.DEVICE_G_R_IR_B)
        assert (x["payload"]["pause"] is True)
        x = self.application.resume()
        assert (x["payload"]["device_id"] == self.application.DEVICE_G_R_IR_B)
        assert (x["payload"]["pause"] is False)

    def test_enable_disable_agc(self):
        x = self.application.enable_agc([self.application.LED_MWL, self.application.LED_GREEN])
        assert (x["payload"]["size"] == 2)
        x = self.application.disable_agc([self.application.LED_MWL, self.application.LED_GREEN])
        assert (x["payload"]["size"] == 2)

    def test_library_configuration(self):
        x = self.application.write_library_configuration([[0x0, 0x12c]])
        assert (x["payload"]["size"] == 1)
        x = self.application.read_library_configuration([0x0])
        assert (x["payload"]["data"] == [['0x0', '0x12C']])

    def test_register(self):
        x = self.application.read_register([0x15, 0x22, 0x2E])
        assert (x["payload"]["size"] == 3)
        x = self.application.write_register([[0x20, 0x1], [0x21, 0x2], [0x2E, 0x3]])
        assert (x["payload"]["size"] == 3)

    def test_set_sampling_frequency(self):
        x = self.application.set_sampling_frequency(100)
        assert (x["payload"]["odr"] == 100)

    def test_stream(self):
        common_test.test_stream(self.application)

    def test_stream_combined(self):
        common_test.test_stream_combined(self.application)

    def test_set_external_stream_sampling_frequency(self):
        x = self.application.set_external_stream_sampling_frequency(50)
        assert (x["payload"]["odr"] == 50)

    # def test_set_external_stream_data(self):
    #     self.application.set_external_stream_data("sdk_pure_python/samples/12104AD0_ADPDAppStream_SlotFChannel2.csv",
    #                                               6, 2, True)
