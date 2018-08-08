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

import pickle

import torch

import complexGrads_utils as CGU

import qucumber
from qucumber.complex_wavefunction import ComplexWavefunction
from qucumber.quantum_reconstruction import QuantumReconstruction
from qucumber.utils import cplx, unitaries


#def generate_visible_space(num_visible, device="cpu"):
#    """Generates all possible visible states.
#
#    :returns: A tensor of all possible spin configurations.
#    :rtype: torch.Tensor
#    """
#    space = torch.zeros((1 << num_visible, num_visible),
#                        device=device, dtype=torch.double)
#    for i in range(1 << num_visible):
#        d = i
#        for j in range(num_visible):
#            d, r = divmod(d, 2)
#            space[i, num_visible - j - 1] = int(r)
#    return space
#
#
#def partition(nn_state, visible_space):
#    """The natural logarithm of the partition function of the RBM.
#
#    :param visible_space: A rank 2 tensor of the entire visible space.
#    :type visible_space: torch.Tensor
#
#    :returns: The natural log of the partition function.
#    :rtype: torch.Tensor
#    """
#    visible_space = visible_space.to(device=nn_state.device)
#    # free_energies = -nn_state.rbm_am.effective_energy(visible_space)
#    # max_free_energy = free_energies.max()
#
#    # f_reduced = free_energies - max_free_energy

#    # logZ = max_free_energy + f_reduced.exp().sum().log()
#    # return logZ.exp()
#    return torch.tensor(
#        nn_state.rbm_am.compute_partition_function(visible_space),
#        device=nn_state.device, dtype=torch.double
#    )
#
#
#def probability(nn_state, v, Z):
#    """Evaluates the probability of the given vector(s) of visible
#    units; NOT RECOMMENDED FOR RBMS WITH A LARGE # OF VISIBLE UNITS
#
#    :param v: The visible states.
#    :type v: torch.Tensor
#    :param Z: The partition function.
#    :type Z: float
#
#    :returns: The probability of the given vector(s) of visible units.
#    :rtype: torch.Tensor
#    """
#    return (nn_state.amplitude(v.to(device=nn_state.device)))**2 / Z
#
#
#def load_target_psi(bases, psi_data):
#    psi_dict = {}
#    D = int(len(psi_data)/float(len(bases)))
#
#    for b in range(len(bases)):
#        psi = torch.zeros(2, D, dtype=torch.double)
#        psi_real = torch.tensor(psi_data[b*D:D*(b+1), 0], dtype=torch.double)
#        psi_imag = torch.tensor(psi_data[b*D:D*(b+1), 1], dtype=torch.double)
#        psi[0] = psi_real
#        psi[1] = psi_imag
#        psi_dict[bases[b]] = psi
#
#    return psi_dict
#
#
#def transform_bases(bases_data):
#    bases = []
#    for i in range(len(bases_data)):
#        tmp = ""
#        for j in range(len(bases_data[i])):
#            if bases_data[i][j] is not " ":
#                tmp += bases_data[i][j]
#        bases.append(tmp)
#    return bases
#
#
#def rotate_psi_full(basis, full_unitary_dict, psi):
#    U = full_unitary_dict[basis]
#    Upsi = cplx.matmul(U, psi)
#    return Upsi
#
#
#def rotate_psi(nn_state, basis, unitary_dict, vis):
#    N = nn_state.num_visible
#    v = torch.zeros(N, dtype=torch.double, device=nn_state.device)
#    psi_r = torch.zeros(2, 1 << N, dtype=torch.double, device=nn_state.device)
#
#    for x in range(1 << N):
#        Upsi = torch.zeros(2, dtype=torch.double, device=nn_state.device)
#        num_nontrivial_U = 0
#        nontrivial_sites = []
#        for j in range(N):
#            if (basis[j] is not 'Z'):
#                num_nontrivial_U += 1
#                nontrivial_sites.append(j)
#        sub_state = generate_visible_space(num_nontrivial_U,
#                                           device=nn_state.device)
#
#        for xp in range(1 << num_nontrivial_U):
#            cnt = 0
#            for j in range(N):
#                if (basis[j] is not 'Z'):
#                    v[j] = sub_state[xp][cnt]
#                    cnt += 1
#                else:
#                    v[j] = vis[x, j]
#
#            U = torch.tensor([1., 0.], dtype=torch.double,
#                             device=nn_state.device)
#            for ii in range(num_nontrivial_U):
#                tmp = unitary_dict[basis[nontrivial_sites[ii]]]
#                tmp = tmp[:,
#                          int(vis[x][nontrivial_sites[ii]]),
#                          int(v[nontrivial_sites[ii]])]
#                U = cplx.scalar_mult(U, tmp)
#
#            Upsi += cplx.scalar_mult(U, nn_state.psi(v))
#
#        psi_r[:, x] = Upsi
#    return psi_r
#
#
#def compute_numerical_NLL(nn_state, data_samples, data_bases, Z,
#                          unitary_dict, vis):
#    NLL = 0
#    batch_size = len(data_samples)
#    b_flag = 0
#    for i in range(batch_size):
#        bitstate = []
#        for j in range(nn_state.num_visible):
#            ind = 0
#            if (data_bases[i][j] != 'Z'):
#                b_flag = 1
#            bitstate.append(int(data_samples[i, j].item()))
#        ind = int("".join(str(i) for i in bitstate), 2)
#        if (b_flag == 0):
#            NLL -= ((probability(nn_state, data_samples[i], Z)).log().item()
#                    / batch_size)
#        else:
#            psi_r = rotate_psi(nn_state, data_bases[i], unitary_dict, vis)
#            NLL -= (cplx.norm(psi_r[:, ind]).log()-Z.log()).item() / batch_size
#    return NLL
#
#
#def compute_numerical_kl(nn_state, psi_dict, vis, Z, unitary_dict, bases):
#    N = nn_state.num_visible
#    psi_r = torch.zeros(2, 1 << N, dtype=torch.double)
#    KL = 0.0
#    for i in range(len(vis)):
#        KL += (cplx.norm(psi_dict[bases[0]][:, i])
#               * cplx.norm(psi_dict[bases[0]][:, i]).log()
#               / float(len(bases)))
#        KL -= (cplx.norm(psi_dict[bases[0]][:, i])
#               * probability(nn_state, vis[i], Z).log().item()
#               / float(len(bases)))
#
#    for b in range(1, len(bases)):
#        psi_r = rotate_psi(nn_state, bases[b], unitary_dict, vis)
#        for ii in range(len(vis)):
#            if(cplx.norm(psi_dict[bases[b]][:, ii]) > 0.0):
#                KL += (cplx.norm(psi_dict[bases[b]][:, ii])
#                       * cplx.norm(psi_dict[bases[b]][:, ii]).log()
#                       / float(len(bases)))
#
#            KL -= (cplx.norm(psi_dict[bases[b]][:, ii])
#                   * cplx.norm(psi_r[:, ii]).log()
#                   / float(len(bases)))
#            KL += (cplx.norm(psi_dict[bases[b]][:, ii])
#                   * Z.log()
#                   / float(len(bases)))
#
#    return KL
#
#
#def algorithmic_gradNLL(qr, data_samples, data_bases, k):
#    # qr.nn_state.set_visible_layer(data_samples)
#    return qr.compute_batch_gradients(k, data_samples,
#                                      data_samples, data_bases)
#
#
#def numeric_gradNLL(nn_state, data_samples, data_bases,
#                    unitary_dict, param, vis, eps):
#    num_gradNLL = []
#    for i in range(len(param)):
#        param[i] += eps
#
#        Z = partition(nn_state, vis)
#        NLL_p = compute_numerical_NLL(nn_state, data_samples, data_bases, Z,
#                                      unitary_dict, vis)
#        param[i] -= 2*eps
#
#        Z = partition(nn_state, vis)
#        NLL_m = compute_numerical_NLL(nn_state, data_samples, data_bases, Z,
#                                      unitary_dict, vis)
#
#        param[i] += eps
#
#        num_gradNLL.append((NLL_p - NLL_m) / (2*eps))
#    return num_gradNLL
#
#
#def numeric_gradKL(param, nn_state, psi_dict, vis, unitary_dict, bases, eps):
#    num_gradKL = []
#    for i in range(len(param)):
#        param[i] += eps
#
#        Z = partition(nn_state, vis)
#        KL_p = compute_numerical_kl(nn_state, psi_dict, vis, Z,
#                                    unitary_dict, bases)
#
#        param[i] -= 2*eps
#
#        Z = partition(nn_state, vis)
#        KL_m = compute_numerical_kl(nn_state, psi_dict, vis, Z,
#                                    unitary_dict, bases)
#        param[i] += eps
#
#        num_gradKL.append((KL_p - KL_m) / (2*eps))
#    return num_gradKL
#
#
#def algorithmic_gradKL(nn_state, psi_dict, vis, unitary_dict, bases):
#    grad_KL = [torch.zeros(nn_state.rbm_am.num_pars,
#                           dtype=torch.double, device=nn_state.device),
#               torch.zeros(nn_state.rbm_ph.num_pars,
#                           dtype=torch.double, device=nn_state.device)]
#    Z = partition(nn_state, vis).to(device=nn_state.device)
#
#    for i in range(len(vis)):
#        grad_KL[0] += (cplx.norm(psi_dict[bases[0]][:, i])
#                       * nn_state.rbm_am.effective_energy_gradient(vis[i])
#                       / float(len(bases)))
#        grad_KL[0] -= (probability(nn_state, vis[i], Z)
#                       * nn_state.rbm_am.effective_energy_gradient(vis[i])
#                       / float(len(bases)))
#
#    for b in range(1, len(bases)):
#        for i in range(len(vis)):
#            rotated_grad = nn_state.gradient(bases[b], vis[i])
#            grad_KL[0] += (cplx.norm(psi_dict[bases[b]][:, i])
#                           * rotated_grad[0]
#                           / float(len(bases)))
#            grad_KL[1] += (cplx.norm(psi_dict[bases[b]][:, i])
#                           * rotated_grad[1]
#                           / float(len(bases)))
#            grad_KL[0] -= (probability(nn_state, vis[i], Z)
#                           * nn_state.rbm_am.effective_energy_gradient(vis[i])
#                           / float(len(bases)))
#    return grad_KL


class TestGradsComplex(unittest.TestCase):

    def percent_diff(self, a, b):
        numerator   = torch.abs(a-b)*100.
        denominator = torch.abs(0.5*(a+b))

        return numerator / denominator

    def assertAlmostEqual(self, a, b, tol, msg=None):
        result = torch.ge(tol*torch.ones_like(torch.abs(a-b)), torch.abs(a-b))
        expect = torch.ones_like(torch.abs(a-b), dtype = torch.uint8)
        self.assertTrue(torch.equal(result, expect), msg=msg)


    def assertPercentDiff(self, a, b, pdiff, msg=None):
        result = torch.ge(pdiff*torch.ones_like(self.percent_diff(a, b)), self.percent_diff(a,b))
        expect = torch.ones_like(result, dtype = torch.uint8)
        self.assertTrue(torch.equal(result, expect), msg=msg)


    def test_allgrads(self):

        k          = 2
        num_chains = 10
        seed       = 1234
        eps        = 1.e-6

        high_tol = torch.tensor(1e-9, dtype = torch.double)
        low_tol  = torch.tensor(1e-5, dtype = torch.double)
        pdiff    = torch.tensor(100, dtype = torch.double)

        with open('test_data.pkl', 'rb') as fin:
            test_data = pickle.load(fin)
    
        qucumber.set_random_seed(seed, cpu=True, gpu=True, quiet=True)

        train_bases   = test_data['2qubits']['train_bases']
        train_samples = torch.tensor(test_data['2qubits']['train_samples'],
                                     dtype=torch.double)

        bases_data     = test_data['2qubits']['bases']
        target_psi_tmp = torch.tensor(test_data['2qubits']['target_psi'],
                                      dtype=torch.double)

        num_visible = train_samples.shape[-1]
        num_hidden  = num_visible

        bases = CGU.transform_bases(bases_data)

        unitary_dict = unitaries.create_dict()
        psi_dict     = CGU.load_target_psi(bases, target_psi_tmp)
        vis          = CGU.generate_visible_space(train_samples.shape[-1])
       
        nn_state      = ComplexWavefunction(unitary_dict, num_visible,
                                            num_hidden, gpu=False)
        qr            = QuantumReconstruction(nn_state)
        device        = qr.nn_state.device
        train_samples = train_samples.to(device=device)
        vis           = vis.to(device=device)
    
        unitary_dict = {b: v.to(device=device) for b, v in unitary_dict.items()}
        psi_dict = {b: v.to(device=device) for b, v in psi_dict.items()}
    
        alg_grad_nll = CGU.algorithmic_gradNLL(qr, train_samples, train_bases, k)
        alg_grad_kl  = CGU.algorithmic_gradKL(qr.nn_state, psi_dict, vis,
                                              unitary_dict, bases)

        for n, net in enumerate(qr.nn_state.networks):
            counter = 0
            print('\n\nRBM: %s' % net)
            rbm = getattr(qr.nn_state, net)
            
            num_grad_kl  = CGU.numeric_gradKL(rbm.weights.view(-1), qr.nn_state,
                                              psi_dict, vis, unitary_dict, bases,
                                              eps)
            num_grad_nll = CGU.numeric_gradNLL(qr.nn_state, train_samples,
                                               train_bases, unitary_dict,
                                               rbm.weights.view(-1), vis, eps)
    
            print("\nTesting weights...")
            print("Numerical KL\tAlg KL\t\t\tNumerical NLL\tAlg NLL")
            for i in range(len(rbm.weights.view(-1))):
                print("{: 10.8f}\t{: 10.8f}\t\t"
                      .format(num_grad_kl[i], alg_grad_kl[n][counter].item()),
                      end="", flush=True)
                print("{: 10.8f}\t{: 10.8f}\t\t"
                      .format(num_grad_nll[i], alg_grad_nll[n][i].item()))
                counter += 1

            #print (num_grad_kl)
            #print (alg_grad_kl[n][:counter])

            self.assertAlmostEqual(num_grad_kl,
                                   alg_grad_kl[n][:counter],
                                   high_tol,
                                   msg="KL grads are not close enough for weights!"
                                  )

            self.assertPercentDiff(num_grad_nll, 
                                   alg_grad_nll[n][:counter],
                                   pdiff,
                                   msg="NLL grads are not close enough for weights!"
                                  )

            num_grad_kl  = CGU.numeric_gradKL(rbm.visible_bias, qr.nn_state, psi_dict,
                                              vis, unitary_dict, bases, eps)
            num_grad_nll = CGU.numeric_gradNLL(qr.nn_state, train_samples, train_bases,
                                               unitary_dict, rbm.visible_bias,
                                               vis, eps)
    
            print("\nTesting visible bias...")
            print("Numerical KL\tAlg KL\t\t\tNumerical NLL\tAlg NLL")
            for i in range(len(rbm.visible_bias)):
                print("{: 10.8f}\t{: 10.8f}\t\t"
                      .format(num_grad_kl[i], alg_grad_kl[n][counter].item()),
                      end="", flush=True)
                print("{: 10.8f}\t{: 10.8f}\t\t"
                      .format(num_grad_nll[i], alg_grad_nll[n][counter].item()))
                counter += 1
   
            self.assertAlmostEqual(num_grad_kl,
                                   alg_grad_kl[n][len(rbm.weights.view(-1)):counter],
                                   high_tol,
                                   msg="KL grads are not close enough for visible biases!"
                                  )

            self.assertPercentDiff(num_grad_nll, 
                                   alg_grad_nll[n][len(rbm.weights.view(-1)):counter],
                                   pdiff,
                                   msg="NLL grads are not close enough for visible biases!"
                                  )
         
 
            num_grad_kl  = CGU.numeric_gradKL(rbm.hidden_bias, qr.nn_state, psi_dict,
                                             vis, unitary_dict, bases, eps)
            num_grad_nll = CGU.numeric_gradNLL(qr.nn_state, train_samples, train_bases,
                                               unitary_dict, rbm.hidden_bias,
                                               vis, eps)

            print("\nTesting hidden bias...")
            print("Numerical KL\tAlg KL\t\t\tNumerical NLL\tAlg NLL")
            for i in range(len(rbm.hidden_bias)):
                print("{: 10.8f}\t{: 10.8f}\t\t"
                      .format(num_grad_kl[i], alg_grad_kl[n][counter].item()),
                      end="", flush=True)
                print("{: 10.8f}\t{: 10.8f}\t\t"
                      .format(num_grad_nll[i], alg_grad_nll[n][counter].item()))
                counter += 1

            self.assertAlmostEqual(num_grad_kl,
                                   alg_grad_kl[n][(len(rbm.weights.view(-1))+
                                                len(rbm.visible_bias)):counter],
                                   high_tol,
                                   msg="KL grads are not close enough for hidden biases!"
                                  )

            self.assertPercentDiff(num_grad_nll, 
                                   alg_grad_nll[n][(len(rbm.weights.view(-1))+
                                                    len(rbm.visible_bias)):counter],
                                   pdiff,
                                   msg="NLL grads are not close enough for hidden biases!"
                                  )  

 
        print('')
    
    
if __name__ == '__main__':
    unittest.main()        
#        k = 2
#        num_chains = 10
#        seed = 1234
#        with open('test_data.pkl', 'rb') as fin:
#            test_data = pickle.load(fin)
#    
#        qucumber.set_random_seed(seed, cpu=True, gpu=True, quiet=True)
#        train_bases = test_data['2qubits']['train_bases']
#        train_samples = torch.tensor(test_data['2qubits']['train_samples'],
#                                     dtype=torch.double)
#        bases_data = test_data['2qubits']['bases']
#        target_psi_tmp = torch.tensor(test_data['2qubits']['target_psi'],
#                                      dtype=torch.double)
#        nh = train_samples.shape[-1]
#        bases = transform_bases(bases_data)
#        unitary_dict = unitaries.create_dict()
#        psi_dict = load_target_psi(bases, target_psi_tmp)
#        vis = generate_visible_space(train_samples.shape[-1])
#        nn_state = ComplexWavefunction(num_visible=train_samples.shape[-1],
#                                       num_hidden=nh, unitary_dict=unitary_dict)
#        qr = QuantumReconstruction(nn_state)
#        eps = 1.e-6
#        run(qr, psi_dict, train_samples, train_bases, unitary_dict, bases,
#            vis, eps, k)