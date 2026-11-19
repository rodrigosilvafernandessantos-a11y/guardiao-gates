"""Resposta interna por extração e critérios fixos; não usa modelo ou oráculo."""
import re


def extract_internal_response(document_id, text):
    clauses = [{'number': int(number), 'text': content} for number, content in
               re.findall(r'^(\d+)\. ([^\n]+)$', text, re.M)]
    table = []
    inside = False
    for line in text.splitlines():
        if line.startswith('|'):
            inside = True
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if not all(re.fullmatch(r'[-:]+', cell) for cell in cells):
                table.append(cells)
        elif inside:
            break
    subject = re.search(r'^\*\*Assunto:\*\* ([^\n]+)', text, re.M)
    body = re.search(r'^\*\*Corpo:\*\* ([^\n]+)', text, re.M)
    conclusion = re.search(r'^Conclusão simulada: ([^\n]+)', text, re.M)
    draft = None
    if subject and body:
        draft = {'subject': subject.group(1), 'body': body.group(1),
                 'clarity_checks': {'subject_present': bool(subject.group(1).strip()),
                                    'creditor_identified': 'Banco Prisma' in body.group(1),
                                    'written_consent_requested': 'consentimento escrito' in body.group(1),
                                    'operational_integration_excluded': 'Não solicitamos integração operacional.' in body.group(1)}}
    return {'document_id': document_id, 'method': 'extracao_e_criterios_fixos', 'response_channel': 'internal',
            'clauses': clauses, 'table': table, 'draft': draft,
            'conclusion': conclusion.group(1) if conclusion else None,
            'model_used': False, 'legal_validation': False}
