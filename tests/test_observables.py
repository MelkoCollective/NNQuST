# Copyright 2018 PIQuIL - All Rights Reserved

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import unittest
import qucumber.observables as observables
from qucumber.nn_states import ComplexWaveFunction

# TODO: add assertions


class TestPauli(unittest.TestCase):
    def test_spinflip(self):
        test_psi = ComplexWaveFunction(2, num_hidden=3)
        test_sample = test_psi.sample(100, num_samples=1000)
        observables.pauli.flip_spin(1, test_sample)

    def test_apply(self):
        test_psi = ComplexWaveFunction(2, num_hidden=3)
        test_sample = test_psi.sample(100, num_samples=1000)
        X = observables.SigmaX()
        X.apply(test_psi, test_sample)

        Y = observables.SigmaY()
        Y.apply(test_psi, test_sample)

        Z = observables.SigmaZ()
        Z.apply(test_psi, test_sample)


if __name__ == "__main__":
    unittest.main()
