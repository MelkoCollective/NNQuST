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

import torch


def make_complex(x, y):
    """A function that combines the real (x) and imaginary (y) parts of a
    vector or a matrix.

    .. note:: x and y must have the same shape. Also, this will not work for
              rank zero tensors.

    :param x: The real part
    :type x: torch.Tensor

    :param y: The imaginary part
    :type y: torch.Tensor

    :returns: The tensor [x,y].
    :rtype: torch.Tensor
    """
    return torch.cat((x.unsqueeze(0), y.unsqueeze(0)), dim=0)


def scalar_mult(x, y):
    """A function that computes the product between complex matrices and scalars,
    complex vectors and scalars or two complex scalars.

    .. note:: If one wishes to do vector-scalar multiplication or matrix-scalar
              multiplication, you must put the vector / matrix as the first
              argument (x).

    :param x: A complex scalar, vector or matrix.
    :type x: torch.Tensor

    :param y: A complex scalar, vector or matrix.
    :type y: torch.Tensor

    :returns: The product between x and y.
    :rtype: torch.Tensor
    """
    z = torch.zeros_like(y)
    z[0] = x[0] * y[0] - x[1] * y[1]
    z[1] = x[0] * y[1] + x[1] * y[0]

    return z


def matmul(x, y):
    """A function that computes complex matrix-matrix and matrix-vector products.

    .. note:: If one wishes to do matrix-vector products, the vector must be
              the second argument (y).

    :param x: A complex matrix.
    :type x: torch.Tensor

    :param y: A complex vector or matrix.
    :type y: torch.Tensor

    :returns: The product between x and y.
    :rtype: torch.Tensor
    """
    if len(list(y.size())) == 2:
        # if one of them is a vector (i.e. wanting to do MV mult)
        z = torch.zeros(2, x.size()[1], dtype=torch.double, device=x.device)
        z[0] = torch.mv(x[0], y[0]) - torch.mv(x[1], y[1])
        z[1] = torch.mv(x[0], y[1]) + torch.mv(x[1], y[0])

    if len(list(y.size())) == 3:
        z = torch.zeros(
            2, x.size()[1], y.size()[2], dtype=torch.double, device=x.device
        )
        z[0] = torch.matmul(x[0], y[0]) - torch.matmul(x[1], y[1])
        z[1] = torch.matmul(x[0], y[1]) + torch.matmul(x[1], y[0])

    return z


def inner_prod(x, y):
    """A function that returns the inner product of two complex vectors,
    x and y (<x|y>).

    :param x: A complex vector.
    :type x: torch.Tensor
    :param y: A complex vector.
    :type y: torch.Tensor

    :raises ValueError: If x and y are not complex vectors with their first
                        dimensions being 2, then the function will not execute.

    :returns: The inner product, :math:`\\langle x\\vert y\\rangle`.
    :rtype: torch.Tensor
    """
    z = torch.zeros(2, dtype=torch.double, device=x.device)

    if len(list(x.size())) == 2 and len(list(y.size())) == 2:
        z[0] = torch.dot(x[0], y[0]) - torch.dot(-x[1], y[1])
        z[1] = torch.dot(x[0], y[1]) + torch.dot(-x[1], y[0])

    if len(list(x.size())) == 1 and len(list(y.size())) == 1:
        z[0] = x[0] * y[0] - (-x[1] * y[1])
        z[1] = x[0] * y[1] + (-x[1] * y[0])

    return z


def outer_prod(x, y):
    """A function that returns the outer product of two complex vectors, x
    and y.

    :param x: A complex vector.
    :type x: torch.Tensor
    :param y: A complex vector.
    :type y: torch.Tensor

    :raises ValueError:	If x and y are not complex vectors with their first
                        dimensions being 2, then the function will not execute.

    :returns: The outer product between x and y,
        :math:`\\vert x \\rangle\\langle y\\vert`.
    :rtype: torch.Tensor
    """
    if len(list(x.size())) != 2 or len(list(y.size())) != 2:
        raise ValueError("An input is not of the right dimension.")

    z = torch.zeros(2, x.size()[1], y.size()[1], dtype=torch.double, device=x.device)
    z[0] = torch.ger(x[0], y[0]) - torch.ger(x[1], -y[1])
    z[1] = torch.ger(x[0], -y[1]) + torch.ger(x[1], y[0])

    return z


def conjugate(x):
    """A function that takes the conjugate transpose of the argument.

    :param x: A complex vector or matrix.
    :type x: torch.Tensor

    :returns: The conjugate of x.
    :rtype: torch.Tensor
    """
    if len(list(x.size())) == 2:
        z = torch.zeros(2, x.size()[1], dtype=torch.double, device=x.device)
        z[0] = x[0]
        z[1] = -x[1]

    if len(list(x.size())) == 3:
        z = torch.zeros(
            2, x.size()[2], x.size()[1], dtype=torch.double, device=x.device
        )
        z[0] = torch.transpose(x[0], 0, 1)
        z[1] = -torch.transpose(x[1], 0, 1)

    return z


def kronecker_prod(x, y):
    """A function that returns the tensor / kronecker product of 2 comlpex
    tensors, x and y.

    :param x: A complex matrix.
    :type x: torch.Tensor
    :param y: A complex matrix.
    :type y: torch.Tensor

    :raises ValueError: If x and y do not have 3 dimensions or their first
                        dimension is not 2, the function cannot execute.

    :returns: The tensorproduct of x and y, :math:`x \\otimes y`.
    :rtype: torch.Tensor
    """
    if len(list(x.size())) != 3 or len(list(y.size())) != 3:
        raise ValueError("An input is not of the right dimension.")

    z = torch.zeros(
        2,
        x.size()[1] * y.size()[1],
        x.size()[2] * y.size()[2],
        dtype=torch.double,
        device=x.device,
    )

    row_count = 0

    for i in range(x.size()[1]):
        for k in range(y.size()[1]):
            column_count = 0
            for j in range(x.size()[2]):
                for l in range(y.size()[2]):

                    z[0][row_count][column_count] = (
                        x[0][i][j] * y[0][k][l] - x[1][i][j] * y[1][k][l]
                    )
                    z[1][row_count][column_count] = (
                        x[0][i][j] * y[1][k][l] + x[1][i][j] * y[0][k][l]
                    )

                    column_count += 1
            row_count += 1

    return z


def scalar_divide(x, y):
    """A function that computes the division of x by y.

    :param x: The numerator (a complex scalar, vector or matrix).
    :type x: torch.Tensor
    :param y: The denominator (a complex scalar).
    :type y: torch.Tensor

    :returns: x / y
    :rtype: torch.Tensor
    """
    if len(list(x.size())) == 2 or len(list(x.size())) == 1:
        y_star = torch.zeros_like(y)
        y_star[0] = y[0]
        y_star[1] = -y[1]

        numerator = scalar_mult(y_star, x)
        denominator = scalar_mult(y, y_star)[0]

    if len(list(x.size())) == 3:
        y_star = torch.zeros_like(y)
        y_star[0] = y[0]
        y_star[1] = -y[1]

        numerator = scalar_mult(y_star, x)
        denominator = scalar_mult(y, y_star)[0]

    return numerator / denominator


def norm(x):
    """A function that returns the norm of the argument.

    :param x: A complex scalar.
    :type x: torch.Tensor

    :returns: :math:`|x|^2`.
    :rtype: torch.Tensor
    """
    return inner_prod(x, x)[0]
