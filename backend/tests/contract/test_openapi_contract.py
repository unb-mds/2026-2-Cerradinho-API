import schemathesis

# gera casos de teste pra todas as rotas documentadas no /openapi.json (RNF04):
# qualquer resposta que fuja do schema declarado, ou erro 500, quebra o teste
schema = schemathesis.pytest.from_fixture("api_schema")


@schema.parametrize()
def test_api_respeita_contrato_openapi(case):
    case.call_and_validate()
