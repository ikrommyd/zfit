#  Copyright (c) 2021 zfit

import numpy as np
import pytest

import zfit
from zfit import z
from zfit.util.exception import SubclassingError


def test_pdf_simple_subclass():
    class SimpleGauss(zfit.pdf.ZPDF):
        _PARAMS = ['mu', 'sigma']

        def _unnormalized_pdf(self, x):
            mu = self.params['mu']
            sigma = self.params['sigma']
            x = z.unstack_x(x)
            return z.exp(-z.square((x - mu) / sigma))

    gauss1 = SimpleGauss(obs='obs1', mu=3, sigma=5)

    prob = gauss1.pdf(np.random.random(size=(10, 1)), norm_range=(-4, 5))
    prob.numpy()

    with pytest.raises(ValueError):
        gauss2 = SimpleGauss('obs1', 1., sigma=5.)
    with pytest.raises(SubclassingError):
        class SimpleGauss2(zfit.pdf.ZPDF):

            def _unnormalized_pdf(self, x):
                mu = self.params['mu']
                sigma = self.params['sigma']
                x = z.unstack_x(x)
                return z.exp(-z.square((x - mu) / sigma))


def test_func_simple_subclass():
    class SimpleGaussFunc(zfit.func.ZFunc):
        _PARAMS = ['mu', 'sigma']

        def _func(self, x):
            mu = self.params['mu']
            sigma = self.params['sigma']
            x = z.unstack_x(x)
            return z.exp(-z.square((x - mu) / sigma))

    gauss1 = SimpleGaussFunc(obs='obs1', mu=3, sigma=5)

    value = gauss1.func(np.random.random(size=(10, 1)))
    value.numpy()

    with pytest.raises(ValueError):
        gauss2 = SimpleGaussFunc('obs1', 1., sigma=5.)
    with pytest.raises(SubclassingError):
        class SimpleGauss2(zfit.func.ZFunc):

            def _func(self, x):
                mu = self.params['mu']
                sigma = self.params['sigma']
                x = z.unstack_x(x)
                return z.exp(-z.square((x - mu) / sigma))
