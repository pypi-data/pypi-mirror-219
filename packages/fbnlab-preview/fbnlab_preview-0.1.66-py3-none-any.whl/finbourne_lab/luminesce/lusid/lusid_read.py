from math import ceil

from finbourne_lab.luminesce.experiment import LumiExperiment
from finbourne_lab.luminesce.lusid.base import LusidLumiLabBase


class LusidLumiLabRead(LusidLumiLabBase):

    def __init__(self, atlas):
        super().__init__(atlas, True)

    def lusid_portfolio_read_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of lusid.portfolio

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 400].
            skip_ensure (bool): whether to skip the ensure step. Defaults to False.

        Returns:
            LumiExperiment: experiment object for the lusid.portfolio measurement.

        """
        skip_ensure = kwargs.get('skip_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 400])

        name = 'lusid_read_portfolio'
        scope = f'fbn-lab_{name}'

        if not skip_ensure:
            print(f'Ensuring content: {scope}')
            self.pf_gen.ensure(scope, rows_rng[-1])

        def build(x, s):
            pf = self.atlas.lusid_portfolio()
            return pf.select('*').where(pf.portfolio_scope == s).limit(x)

        return LumiExperiment(name, build, rows_rng, scope)

    def lusid_instrument_read_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of lusid.instrument

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            skip_ensure (bool): whether to skip the ensure step. Defaults to False.

        Returns:
            LumiExperiment: experiment object for the lusid.instrument measurement.

        """
        skip_ensure = kwargs.get('skip_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])

        name = 'lusid_read_instrument'
        scope = f'fbn-lab_{name}'

        if not skip_ensure:
            print(f'Ensuring content: {scope}')
            self.in_gen.ensure(scope, rows_rng[-1])

        def build(x, s):
            ins = self.atlas.lusid_instrument()
            return ins.select('*').where(ins.scope == s).limit(x)

        return LumiExperiment(name, build, rows_rng, scope)

    def lusid_portfolio_txn_read_measurement(self, **kwargs):
        """Make a list of experiments for measuring the performance of lusid.portfolio.txn over different shape of data.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            skip_ensure (bool): whether to skip the ensure step. Defaults to False.
            txns_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of txns per portfolio. Defaults to 100, 1000, 10000.

        Notes:
            Data shape is the number of portfolios the txns are spread over. This is parameterised as the number of txns
            per portfolio in a scope. A test scope will be created for a given shape for each experiment.


        Returns:
            List[LumiExperiment]: experiment list for measuring txn read performance over different shaped data.

        """
        skip_ensure = kwargs.get('skip_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        rows_max = max(rows_rng)

        txns_per_pf_set = kwargs.get('txns_per_pf', [10000, 1000, 100])

        experiments = []

        txn = self.atlas.lusid_portfolio_txn()

        for txns_per_pf in txns_per_pf_set:
            name = f'lusid_read_txn_{txns_per_pf}'
            scope = f'fbn-lab_{name}'

            n_portfolios = ceil(rows_max / txns_per_pf)
            if not skip_ensure:
                print(f'Ensuring content: {scope}')
                self.pf_gen.ensure(scope, n_portfolios)
                self.tx_gen.ensure(scope, n_portfolios, txns_per_pf)

            def build(x, s):
                return txn.select('*').where(txn.portfolio_scope == s).limit(x)

            ex = LumiExperiment(name, build, rows_rng, scope)
            experiments.append(ex)

        return experiments

    def lusid_portfolio_holding_read_measurement(self, **kwargs):
        """Make a list of experiments for measuring the performance of lusid.portfolio.holding over different shape of data.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            skip_ensure (bool): whether to skip the ensure step. Defaults to False.
            hlds_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of holdings per portfolio. Defaults to 100, 1000, 10000.

        Notes:
            Data shape is the number of portfolios the holdings are spread over. This is parameterised as the number of
            holdings per portfolio in a scope. A test scope will be created for a given shape for each experiment.


        Returns:
            List[LumiExperiment]: experiment list for measuring holdings read performance over different shaped data.

        """
        skip_ensure = kwargs.get('skip_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        rows_max = max(rows_rng)

        hlds_per_pf_set = kwargs.get('hlds_per_pf', [10000, 1000, 100])

        experiments = []

        hld = self.atlas.lusid_portfolio_holding()

        for hlds_per_pf in hlds_per_pf_set:
            name = f'lusid_read_hld_{hlds_per_pf}'
            scope = f'fbn-lab_{name}'

            n_portfolios = ceil(rows_max / hlds_per_pf)
            if not skip_ensure:
                print(f'Ensuring content: {scope}')
                self.pf_gen.ensure(scope, n_portfolios)
                self.hl_gen.ensure(scope, n_portfolios, hlds_per_pf)

            def build(x, s):
                return hld.select('*').where(hld.portfolio_scope == s).limit(x)

            ex = LumiExperiment(name, build, rows_rng, scope)
            experiments.append(ex)

        return experiments
