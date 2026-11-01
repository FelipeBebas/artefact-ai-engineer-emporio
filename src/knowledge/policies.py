"""Base de conhecimento estruturada e determinística das políticas da loja (Zero-Flake)."""

from enum import Enum
from typing import Dict, Optional, Union


class TopicoPolitica(str, Enum):
    """Tópicos oficiais cobertos pelo Manual de Políticas da Empório da Música."""

    SOBRE_A_LOJA = "sobre_a_loja"
    HORARIOS_FUNCIONAMENTO = "horarios_funcionamento"
    FORMAS_PAGAMENTO = "formas_pagamento"
    REGRAS_PARCELAMENTO = "regras_parcelamento"
    TROCAS_DEVOLUCOES = "trocas_devolucoes"
    POLITICA_FRETE = "politica_frete"
    PROMOCOES_REGRAS = "promocoes_regras"
    GARANTIA = "garantia"
    LGPD_PRIVACIDADE = "lgpd_privacidade"
    ATENDIMENTO_WHATSAPP = "atendimento_whatsapp"


POLITICAS_MANUAL: Dict[TopicoPolitica, str] = {
    TopicoPolitica.SOBRE_A_LOJA: (
        "SOBRE A EMPÓRIO DA MÚSICA:\n"
        "- Fundada em 2008 em Campo Grande/MS, com mais de 15 anos de atuação.\n"
        "- Catálogo com mais de 300 instrumentos nacionais e internacionais (guitarras, baixos, "
        "violões, baterias, teclados, sopros, cordas orquestrais e ukuleles).\n"
        "- ESCOPO ESTRITO: Trabalhamos EXCLUSIVAMENTE com instrumentos musicais. NÃO comercializamos "
        "acessórios como cordas, palhetas, cabos, cases, pedais ou amplificadores.\n"
        "- Dados: CNPJ 12.345.678/0001-90 | Endereço: Rua 14 de Maio, 3200 — Centro, Campo Grande - MS, CEP 79202-333.\n"
        "- Contatos: Telefone/WhatsApp (67) 3341-4444 | E-mail: contato@emporiodamusica.com.br."
    ),
    TopicoPolitica.HORARIOS_FUNCIONAMENTO: (
        "HORÁRIO DE FUNCIONAMENTO (Presencial e WhatsApp):\n"
        "- Segunda a Sexta-feira: 09:00 às 18:00.\n"
        "- Sábado: 09:00 às 13:00.\n"
        "- Domingo e Feriados: Fechado.\n"
        "- Fora do expediente, o atendimento automático informa o horário de retorno da equipe."
    ),
    TopicoPolitica.FORMAS_PAGAMENTO: (
        "FORMAS DE PAGAMENTO:\n"
        "- PIX: À vista com 5% de desconto sobre o preço de tabela (não cumulativo com promoções ativas).\n"
        "- Cartão de Débito: À vista (todas as bandeiras aceitas).\n"
        "- Cartão de Crédito: Até 12x sem juros (respeitando parcelas mínimas).\n"
        "- Boleto Bancário: À vista, compensação em até 3 dias úteis."
    ),
    TopicoPolitica.REGRAS_PARCELAMENTO: (
        "REGRAS DE PARCELAMENTO NO CARTÃO DE CRÉDITO:\n"
        "- Até 3x: sem juros, sem valor mínimo de parcela (exceto abaixo de R$ 50,00).\n"
        "- De 4x a 6x: sem juros, com parcela mínima de R$ 80,00.\n"
        "- De 7x a 12x: sem juros, com parcela mínima de R$ 100,00.\n"
        "- Combinação de formas de pagamento (ex: PIX + Cartão): permitida para compras acima de R$ 2.000,00."
    ),
    TopicoPolitica.TROCAS_DEVOLUCOES: (
        "POLÍTICA DE TROCAS E DEVOLUÇÕES (CDC - Lei nº 8.078/90):\n"
        "1. Direito de Arrependimento (Compras Online):\n"
        "   - Prazo de até 7 (sete) dias corridos após o recebimento do produto, sem necessidade de justificativa.\n"
        "   - Produto deve estar na embalagem original, sem sinais de uso, com todos os acessórios e manuais.\n"
        "   - Reembolso na mesma forma de pagamento original em até 10 dias úteis.\n"
        "   - Frete de devolução por conta da loja em caso de arrependimento.\n"
        "2. Trocas por Defeito:\n"
        "   - Até 30 (trinta) dias corridos após a compra direto com a loja. Após 30 dias, acionar garantia do fabricante.\n"
        "   - Danos por mau uso, quedas, umidade excessiva ou modificações não autorizadas não são cobertos.\n"
        "3. Trocas por Preferência (cor, modelo):\n"
        "   - Permitidas em até 7 dias, produto perfeito na embalagem original, mediante disponibilidade.\n"
        "4. Itens NÃO elegíveis para troca: Instrumentos com regulagem/setup sob encomenda, produtos em liquidação "
        "com aviso de 'venda final' e boquilhas de instrumentos de sopro (higiene)."
    ),
    TopicoPolitica.POLITICA_FRETE: (
        "POLÍTICA DE FRETE E ENTREGAS:\n"
        "1. Região Metropolitana de Campo Grande/MS:\n"
        "   - Frete GRÁTIS para pedidos acima de R$ 500,00.\n"
        "   - Taxa fixa de R$ 35,00 para pedidos abaixo de R$ 500,00.\n"
        "   - Prazo: 1 a 3 dias úteis (entrega por motoboy próprio, com aviso por telefone antes da entrega).\n"
        "2. Outras Cidades (Correios e Jadlog):\n"
        "   - PAC (Correios): 5 a 12 dias úteis (com rastreamento e seguro incluído).\n"
        "   - SEDEX (Correios): 2 a 5 dias úteis (com rastreamento e seguro incluído).\n"
        "   - Jadlog (.package): 3 a 8 dias úteis (com rastreamento e seguro incluído).\n"
        "   - Código de rastreamento: Formato BR + 9 caracteres alfanuméricos + BR (ex: BR4K7M2X9P1BR)."
    ),
    TopicoPolitica.PROMOCOES_REGRAS: (
        "REGRAS DE PROMOÇÕES E DESCONTOS:\n"
        "- Campanhas do ano: Aniversário da Loja (Agosto: 10% a 25%), Black Friday (Novembro: 15% a 30%), "
        "Volta às Aulas (Fevereiro), Queima de Estoque, Semana do Músico (Novembro).\n"
        "- Cumulatividade: Promoções NÃO são cumulativas. O desconto de PIX (5%) NÃO se aplica sobre preços promocionais.\n"
        "- Estoque: Promoções sujeitas a disponibilidade. Produtos esgotados não geram rain check (reserva de preço).\n"
        "- Transparência: Preço promocional sempre acompanhado do preço original e percentual de desconto."
    ),
    TopicoPolitica.GARANTIA: (
        "GARANTIA DE PRODUTOS:\n"
        "- Garantia Legal: 90 (noventa) dias contra defeitos de fabricação (Código de Defesa do Consumidor).\n"
        "- Garantia do Fabricante: Varia de 6 meses a 2 anos conforme certificado que acompanha o instrumento.\n"
        "- O que NÃO é coberto: Desgaste natural de peças (trastes, cordas, feltros, palhetas de sopro), danos "
        "por quedas ou mau uso, umidade extrema, consertos por terceiros não autorizados ou danos estéticos."
    ),
    TopicoPolitica.LGPD_PRIVACIDADE: (
        "PRIVACIDADE E DADOS (LGPD - Lei nº 13.709/2018):\n"
        "- Dados pessoais (nome, telefone, e-mail, endereço) usados unicamente para processamento de pedidos, "
        "rastreamento, suporte e notas fiscais.\n"
        "- Não compartilhamos dados com terceiros para marketing. Cliente pode solicitar exclusão a qualquer momento."
    ),
    TopicoPolitica.ATENDIMENTO_WHATSAPP: (
        "DIRETRIZES DE ATENDIMENTO:\n"
        "- Tom de voz: Informal mas profissional. Amigo que entende de música, acolhedor e atencioso.\n"
        "- Precisão: Nunca informar preços, estoques ou prazos sem consultar a base de dados.\n"
        "- Escopo: Loja comercializa exclusivamente instrumentos musicais. Pedidos de acessórios (cordas, cabos, "
        "palhetas, pedais, amplificadores, cases) devem ser educadamente redirecionados para lojas parceiras."
    ),
}

# Mapeamento para resolução de sinônimos/termos livres
KEYWORD_MAPPING = {
    "horario": TopicoPolitica.HORARIOS_FUNCIONAMENTO,
    "horarios": TopicoPolitica.HORARIOS_FUNCIONAMENTO,
    "aberto": TopicoPolitica.HORARIOS_FUNCIONAMENTO,
    "fechado": TopicoPolitica.HORARIOS_FUNCIONAMENTO,
    "pagamento": TopicoPolitica.FORMAS_PAGAMENTO,
    "pix": TopicoPolitica.FORMAS_PAGAMENTO,
    "cartao": TopicoPolitica.FORMAS_PAGAMENTO,
    "boleto": TopicoPolitica.FORMAS_PAGAMENTO,
    "parcela": TopicoPolitica.REGRAS_PARCELAMENTO,
    "parcelamento": TopicoPolitica.REGRAS_PARCELAMENTO,
    "juros": TopicoPolitica.REGRAS_PARCELAMENTO,
    "troca": TopicoPolitica.TROCAS_DEVOLUCOES,
    "trocar": TopicoPolitica.TROCAS_DEVOLUCOES,
    "devolucao": TopicoPolitica.TROCAS_DEVOLUCOES,
    "devolver": TopicoPolitica.TROCAS_DEVOLUCOES,
    "arrependi": TopicoPolitica.TROCAS_DEVOLUCOES,
    "arrependimento": TopicoPolitica.TROCAS_DEVOLUCOES,
    "frete": TopicoPolitica.POLITICA_FRETE,
    "entrega": TopicoPolitica.POLITICA_FRETE,
    "jadlog": TopicoPolitica.POLITICA_FRETE,
    "correios": TopicoPolitica.POLITICA_FRETE,
    "pac": TopicoPolitica.POLITICA_FRETE,
    "sedex": TopicoPolitica.POLITICA_FRETE,
    "rastreio": TopicoPolitica.POLITICA_FRETE,
    "promocao": TopicoPolitica.PROMOCOES_REGRAS,
    "promocoes": TopicoPolitica.PROMOCOES_REGRAS,
    "desconto": TopicoPolitica.PROMOCOES_REGRAS,
    "black friday": TopicoPolitica.PROMOCOES_REGRAS,
    "garantia": TopicoPolitica.GARANTIA,
    "defeito": TopicoPolitica.GARANTIA,
    "estragou": TopicoPolitica.GARANTIA,
    "quebrou": TopicoPolitica.GARANTIA,
    "lgpd": TopicoPolitica.LGPD_PRIVACIDADE,
    "dados": TopicoPolitica.LGPD_PRIVACIDADE,
    "privacidade": TopicoPolitica.LGPD_PRIVACIDADE,
    "endereco": TopicoPolitica.SOBRE_A_LOJA,
    "loja": TopicoPolitica.SOBRE_A_LOJA,
    "onde fica": TopicoPolitica.SOBRE_A_LOJA,
    "whatsapp": TopicoPolitica.ATENDIMENTO_WHATSAPP,
    "acessorio": TopicoPolitica.ATENDIMENTO_WHATSAPP,
    "acessorios": TopicoPolitica.ATENDIMENTO_WHATSAPP,
}


def resolver_topico(termo: Union[TopicoPolitica, str]) -> Optional[TopicoPolitica]:
    """Resolve uma string ou Enum para o TopicoPolitica canônico."""
    if isinstance(termo, TopicoPolitica):
        return termo

    termo_str = str(termo).lower().strip()

    # Tenta casamento exato com os valores de TopicoPolitica
    for topico in TopicoPolitica:
        if termo_str == topico.value:
            return topico

    # Tenta casamento por palavra-chave ou sinônimo
    for key, topico in KEYWORD_MAPPING.items():
        if key in termo_str:
            return topico

    return None


def consultar_politica(topico: Union[TopicoPolitica, str]) -> str:
    """Retorna o texto oficial e determinístico do manual para o tópico solicitado."""
    topico_resolvido = resolver_topico(topico)
    if topico_resolvido and topico_resolvido in POLITICAS_MANUAL:
        return POLITICAS_MANUAL[topico_resolvido]

    # Fallback se não encontrar o tópico exato
    return (
        "Informação não localizada no manual de políticas para o tópico informado. "
        "Tópicos disponíveis: sobre_a_loja, horarios_funcionamento, formas_pagamento, "
        "regras_parcelamento, trocas_devolucoes, politica_frete, promocoes_regras, garantia, lgpd_privacidade."
    )
