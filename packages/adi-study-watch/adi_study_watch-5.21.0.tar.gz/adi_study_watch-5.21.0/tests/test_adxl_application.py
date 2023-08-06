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


def adxl_callback(data):
    print(data)


class TestADXLApplication(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.application = SDK("COM4").get_adxl_application()
        cls.application.set_callback(adxl_callback)

    def test_read_register(self):
        x = self.application.read_register([0x20, 0x1, 0x2])
        print(x)
        assert (x["payload"]["size"] == 3)
        assert (type(x["payload"]["data"]) == list)

    def test_write_register(self):
        x = self.application.write_register([[0x20, 0x1], [0x21, 0x2], [0x2E, 0x3]])
        assert (x["payload"]["size"] == 3)
        assert (x["payload"]["data"] == [['0x20', '0x1'], ['0x21', '0x2'], ['0x2E', '0x3']])

    def test_get_decimation_factor(self):
        x = self.application.get_decimation_factor()
        assert (type(x["payload"]["decimation_factor"]) == int)

    def test_set_decimation_factor(self):
        x = self.application.set_decimation_factor(2)
        assert (x["payload"]["decimation_factor"] == 2)

    def test_get_device_configuration(self):
        x = self.application.get_device_configuration()
        assert (type(x["payload"]["size"]) == int)
        assert (type(x["payload"]["data"]) == list)

    def test_load_configuration(self):
        x = self.application.load_configuration(self.application.DEVICE_362)
        assert (x["payload"]["device_id"] == self.application.DEVICE_362)

    def test_get_sensor_status(self):
        x = self.application.get_sensor_status()
        assert (type(x["payload"]["num_subscribers"]) == int)
        assert (type(x["payload"]["num_start_registered"]) == int)

    def test_device_configuration_block(self):
        x = self.application.write_device_configuration_block([[0x20, 2], [0x21, 0x1]])
        assert (x["payload"]["size"] == 0)
        x = self.application.read_device_configuration_block()
        assert (x["payload"]["data"] == [['0x20', '0x2'], ['0x21', '0x1']])
        x = self.application.delete_device_configuration_block()
        assert (x["payload"]["size"] == 0)

    def test_stream(self):
        common_test.test_stream(self.application)

    def test_stream_combined(self):
        common_test.test_stream_combined(self.application)
