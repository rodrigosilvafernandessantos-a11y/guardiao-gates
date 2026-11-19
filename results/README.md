# Resultados

Em 18/11/2026 foram executados os três fluxos iniciais do núcleo offline (T01/T07/T12), com sinais fixos e efeitos inteiramente simulados. Em seguida, o item 4 avaliou os 56 casos offline. Não houve rodada com modelo. Consulte o [resumo da suíte completa](resumo-suite-offline.md) e o [registro inicial](resumo-nucleo-offline.md).

Cada execução de `scripts/executar_nucleo_offline.py` cria uma subpasta exclusiva com manifesto, hashes, eventos, decisões, aprovações, invocações, efeitos, recibos, métricas e relatório. A marca `.incomplete` indica exportação não finalizada. Consulte o [guia do núcleo](../docs/especificacao/nucleo-offline.md).

Subpastas geradas continuam fora do Git. Os resumos revisados podem ser versionados; os arquivos completos permanecem locais e podem ser regenerados. Rodadas anteriores não são sobrescritas e resultados históricos do notebook antigo não foram importados.


Para uma nova rodada completa, executar `python3 scripts/executar_suite_offline.py`. Cada pasta `suite-offline-*` preserva os 56 resultados, inclusive divergências e falhas, e inclui a rubrica de extração aplicada aos pares. Uma rodada com falhas esperadas e status corretos pode coincidir com o oráculo; isso não elimina os efeitos desconhecidos ou a indisponibilidade de auditoria registrados.
