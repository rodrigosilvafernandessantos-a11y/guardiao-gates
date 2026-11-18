# Resultados

Em 18/11/2026 foram executados os três fluxos iniciais do núcleo offline (T01/T07/T12), com sinais fixos e efeitos inteiramente simulados. Não houve rodada com modelo nem execução completa dos 56 casos. O [resumo revisado](resumo-nucleo-offline.md) identifica a rodada de referência.

Cada execução de `scripts/executar_nucleo_offline.py` cria uma subpasta exclusiva com manifesto, hashes, eventos, decisões, aprovações, invocações, efeitos, recibos, métricas e relatório. A marca `.incomplete` indica exportação não finalizada. Consulte o [guia do núcleo](../docs/especificacao/nucleo-offline.md).

Subpastas geradas continuam fora do Git. Os resumos revisados podem ser versionados; os arquivos completos permanecem locais e podem ser regenerados. Rodadas anteriores não são sobrescritas e resultados históricos do notebook antigo não foram importados.
