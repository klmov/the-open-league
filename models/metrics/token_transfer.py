from models.metric import Metric, CalculationContext, TonalyticaMetricImpl


class TokenTransferTonalyticaImpl(TonalyticaMetricImpl):

    def calculate(self, context: CalculationContext, metric):
        destinations = "\nor\n".join(map(lambda addr: f"jt.destination_owner  = '{addr}'", metric.destinations))
        jetton_masters = "\nor\n".join(map(lambda addr: f"jt.destination_owner  = '{addr}'", metric.jetton_masters))

        return f"""
        select jt.msg_id as id, '{context.project.name}' as project, jt.source_owner as user_address
        from jetton_transfers_local jt
        WHERE (
            {destinations}
        )
        AND (
            {jetton_masters}
        )
        """


"""
TEP-74 token (jetton) transfer, allows to specify the list of destinations and the list of jetton addresses
"""
class TokenTransfer(Metric):
    def __init__(self, description, jetton_masters=[], destinations=[], is_custodial=False):
        Metric.__init__(self, description, [TokenTransferTonalyticaImpl()])
        self.jetton_masters = jetton_masters
        self.is_custodial = is_custodial
        self.destinations = destinations

