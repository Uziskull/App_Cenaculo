from models import Poll, ActivePoll, Vote, db

# ----------------------------------------- #
# Erros
# ----------------------------------------- #

class PollError(Exception):
    pass

class DuplicateVoteError(PollError):
    def __init__(self):
        super().__init__("Já votaste nessa proposta!")

class VotingClosedError(PollError):
    def __init__(self, has_ended):
        str_end = "ainda não começou!"
        if has_ended:
            str_end = "já acabou!"
        super().__init__("A votação para essa proposta " + str_end)

class VotingPeriodError(PollError):
    def __init__(self):
        super().__init__("Não existem votações a decorrer!")

class PollNotFoundError(PollError):
    def __init__(self):
        super().__init__("Essa proposta não existe!")

class BadVoteError(PollError):
    def __init__(self, vote):
        super().__init__(f"Tipo de voto inválido: {vote}")

class SecondRoundAbstentionError(PollError):
    def __init__(self):
        super().__init__("Esta proposta está em segunda volta, abstenção de voto não é permitido!")

# -----------------------------------

class PollOrderingError(PollError):
    def __init__(self):
        super().__init__("Essa ordem de proposta é inválida!")

class PollAlreadyOpenError(PollError):
    def __init__(self):
        super().__init__("Já existe uma proposta aberta!")

class PollNotOpenError(PollError):
    def __init__(self):
        super().__init__("Essa proposta não está aberta!")

class PollDeleteOpenError(PollError):
    def __init__(self):
        super().__init__("Não é permitido apagar uma proposta aberta!")

# ----------------------------------------- #
# Variáveis
# ----------------------------------------- #

# inseridas globalmente, para a pagina de voto saber que votos existem
VOTOS = ["SIM", "NAO", "ABSTER"]

ESTADOS = ["APROVADO", "REPROVADO", "2VOLTA"]

# ----------------------------------------- #
# WebApp
# ----------------------------------------- #

def vote_with_token(token: str, vote: str, poll_id: str):
    # verificar se voto é válido
    vote_num = None
    try:
        vote_num = VOTOS.index(vote.upper())
    except ValueError:
        raise BadVoteError(vote)

    # verificar se existem propostas abertas
    current_poll = get_current_poll()
    if current_poll is None:
        raise VotingPeriodError()

    # verificar se proposta existe
    #possible_poll = Poll.query.get(poll_id)
    possible_poll = db.session.execute(db.select(Poll).where(Poll.id == poll_id)).scalar()
    if possible_poll is None:
        raise PollNotFoundError()

    # verificar se proposta permite abstenções
    if possible_poll.status == ESTADOS.index("2VOLTA") and vote_num == VOTOS.index("ABSTER"):
        raise SecondRoundAbstentionError()

    # verificar se proposta está aberta a votos
    if current_poll.id != poll_id:
        raise VotingClosedError(possible_poll.status not in [None, ESTADOS.index("2VOLTA")])
        # has_previous_votes = len(possible_poll.votes) > 0
        # raise VotingClosedError(has_previous_votes)

    # verificar se utilizador já votou
    if already_voted(token, poll_id):
        raise DuplicateVoteError()
    
    db.session.add(Vote(token, poll_id, vote_num))
    db.session.commit()

def already_voted(token: str, poll_id: str):
    #uv = Vote.query.filter_by(user_token=token, poll_id=poll_id).first()
    uv = db.session.execute(db.select(Vote).where(Vote.user_token == token).where(Vote.poll_id == poll_id)).scalar()
    return uv is not None

def get_current_poll():
    #active_poll = ActivePoll.query.first()
    active_poll = db.session.execute(db.select(ActivePoll)).scalar()
    if active_poll is None:
        return None
    #return Poll.query.get(active_poll.poll_id)
    return db.session.execute(db.select(Poll).where(Poll.id == active_poll[0].poll_id)).scalar()

def get_all_polls():
    #return Poll.query.order_by(Poll.order).all()
    return db.session.execute(db.select(Poll).order_by(Poll.order)).scalars().all()

def get_all_polls_and_results():
    # este gatafunho devolve todas as propostas e o seu número de votos positivos/negativos/neutros
    # ordem de votos é a estabelecida em 'VOTOS': sim, não, abster
    #return db.Query([
    #        Poll.id,
    #        Poll.description,
    #        Poll.order,
    #        db.func.count(db.case(
    #            [((Vote.vote_option == 0), Vote.user_token)],
    #            else_=db.literal_column("NULL")
    #        )).label(VOTOS[0].lower()),
    #        db.func.count(db.case(
    #            [((Vote.vote_option == 1), Vote.user_token)],
    #            else_=db.literal_column("NULL")
    #        )).label(VOTOS[1].lower()),
    #        db.func.count(db.case(
    #            [((Vote.vote_option == 2), Vote.user_token)],
    #            else_=db.literal_column("NULL")
    #        )).label(VOTOS[2].lower()),
    #        Poll.status],
    #        session=db.session) \
    #    .select_from(Poll) \
    #    .join(Vote, isouter=True) \
    #    .group_by(Poll.id, Poll.description, Poll.order) \
    #    .order_by(Poll.order) \
    #    .all()
    return db.session.execute(
        db.select(
            Poll.id,
            Poll.description,
            Poll.order,
            db.func.count(db.case(
                (Vote.vote_option == 0, Vote.user_token),
                else_=db.literal_column("NULL")
            )).label(VOTOS[0].lower()),
            db.func.count(db.case(
                (Vote.vote_option == 1, Vote.user_token),
                else_=db.literal_column("NULL")
            )).label(VOTOS[1].lower()),
            db.func.count(db.case(
                (Vote.vote_option == 2, Vote.user_token),
                else_=db.literal_column("NULL")
            )).label(VOTOS[2].lower()),
            Poll.status) \
        .select_from(Poll) \
        .join(Vote, isouter=True) \
        .group_by(Poll.id, Poll.description, Poll.order) \
        .order_by(Poll.order)
    ).all()

# ----------------------------------------- #
# GUI
# ----------------------------------------- #

def count_polls() -> int:
    #return db.session.query(Poll).count()
    return len(db.session.execute(db.select(Poll)).scalars().all())

def create_poll(order: int, description: str) -> Poll:
    # adicionar proposta no final da lista
    new_poll = Poll(order, description)
    db.session.add(new_poll)
    db.session.flush()
    db.session.commit()
    return new_poll

def get_votes_for(poll_id: str):
    #return db.Query([
    #        db.func.count(db.case(
    #            [((Vote.vote_option == 0), Vote.user_token)],
    #            else_=db.literal_column("NULL")
    #        )).label(VOTOS[0].lower()),
    #        db.func.count(db.case(
    #            [((Vote.vote_option == 1), Vote.user_token)],
    #            else_=db.literal_column("NULL")
    #        )).label(VOTOS[1].lower()),
    #        db.func.count(db.case(
    #            [((Vote.vote_option == 2), Vote.user_token)],
    #            else_=db.literal_column("NULL")
    #        )).label(VOTOS[2].lower())],
    #        session=db.session) \
    #    .select_from(Vote) \
    #    .filter(Vote.poll_id == poll_id) \
    #    .one()
    return db.session.execute(
        db.select(
            db.func.count(db.case(
                ((Vote.vote_option == 0), Vote.user_token),
                else_=db.literal_column("NULL")
            )).label(VOTOS[0].lower()),
            db.func.count(db.case(
                ((Vote.vote_option == 1), Vote.user_token),
                else_=db.literal_column("NULL")
            )).label(VOTOS[1].lower()),
            db.func.count(db.case(
                ((Vote.vote_option == 2), Vote.user_token),
                else_=db.literal_column("NULL")
            )).label(VOTOS[2].lower())) \
        .select_from(Vote)
        .filter(Vote.poll_id == poll_id)
    ).one()

def order_poll(poll_id: str, new_order: int) -> None:
    polls = get_all_polls()

    # verificar se ordem está dentro dos limites
    if new_order <= 0 or new_order > len(polls):
        raise PollOrderingError()

    poll_to_change = [p for p in polls if p.id == poll_id]
    # verificar se proposta existe
    if len(poll_to_change) == 0:
        raise PollNotFoundError()
    poll_to_change = poll_to_change[0]

    # não efetuar alterações se ordem corresponder à ordem atual da proposta
    if poll_to_change.order == new_order:
        return
    
    # 1. obter tudo entre proposta a alterar e proposta com a ordem pretendida
    poll_going_up = poll_to_change.order > new_order
    polls_to_change = polls[poll_to_change.order-1:new_order-1]
    if poll_going_up:
        polls_to_change = polls[new_order-1:poll_to_change.order-1]
    # 2. alterar ordem de proposta a alterar, e dar shift de tudo para +1 ou -1, conforme
    poll_to_change.order = new_order
    map(lambda p: p.order + (1 if poll_going_up else -1), polls_to_change)
    # 3. update all
    for p in polls_to_change:
        db.session.merge(p)
    db.session.commit()

def edit_poll(poll_id: str, new_description: str) -> None:
    #poll = Poll.query.get(poll_id)
    poll = db.session.execute(db.select(Poll).where(Poll.id == poll_id)).scalar()
    if poll is None:
        raise PollNotFoundError()
    
    if poll.description == new_description:
        return

    poll.description = new_description
    db.session.merge(poll)
    db.session.commit()

def delete_poll(poll_id: str) -> None:
    #poll = Poll.query.get(poll_id)
    poll = db.session.execute(db.select(Poll).where(Poll.id == poll_id)).scalar()
    if poll is None:
        raise PollNotFoundError()

    #active_poll = ActivePoll.query.first()
    active_poll = db.session.execute(db.select(ActivePoll)).scalar()
    if active_poll is not None and active_poll.poll_id == poll_id:
        raise PollDeleteOpenError()

    # limpar votos associados com voto
    #Vote.query.filter(Vote.poll_id == poll_id).delete()
    db.session.delete(
        db.session.execute(db.select(Vote).where(Vote.poll_id == poll_id)).scalar()
    )

    deleted_order = poll.order
    db.session.delete(poll)

    polls = get_all_polls()
    if deleted_order < len(polls):
        polls_to_change = polls[deleted_order - 1:]
        for p in polls_to_change:
            p.order -= 1
            db.session.merge(p)

    db.session.commit()

def open_poll(poll_id: str) -> None:
    #active_poll = ActivePoll.query.first()
    active_poll = db.session.execute(db.select(ActivePoll)).scalar()
    if active_poll is not None:
        raise PollAlreadyOpenError()
    
    #poll = Poll.query.get(poll_id)
    poll = db.session.execute(db.select(Poll).where(Poll.id == poll_id)).scalar()
    if poll is None:
        raise PollNotFoundError()

    if poll.status not in [None, ESTADOS.index("2VOLTA")]:
        raise VotingClosedError(True)
    elif poll.status == ESTADOS.index("2VOLTA"):
        # se for 2ª volta, limpar votos existentes
        #Vote.query.filter(Vote.poll_id == poll_id).delete()
        db.session.delete(
            db.session.execute(db.select(Vote).where(Vote.poll_id == poll_id)).scalar()
        )
        db.session.commit()

    active_poll = ActivePoll(poll_id)
    db.session.add(active_poll)
    db.session.commit()


def close_poll(poll_id: str) -> None:
    #active_poll = ActivePoll.query.first()
    active_poll = db.session.execute(db.select(ActivePoll)).scalar()
    if active_poll is None:
        raise VotingPeriodError()
    
    if active_poll.poll_id != poll_id:
        raise PollNotOpenError()

    db.session.delete(active_poll)
    db.session.commit()

def count_votes(poll_id: str) -> Poll:
    #poll = Poll.query.get(poll_id)
    poll = db.session.execute(db.select(Poll).where(Poll.id == poll_id)).scalar()
    if poll is None:
        raise PollNotFoundError()

    if poll.status not in [None, ESTADOS.index("2VOLTA")]:
        raise VotingClosedError(True)

    votes = get_votes_for(poll_id)
    for i in range(len(VOTOS)):
        if votes[i] > 0:
            # se já alguém votou

            # técnica de votação: 50+1, caso não seja aprovada/reprovada vai a segunda volta sem abstenção
            # se status já for 2ª volta, é caso de empate em segunda volta: proposta reprovada
            final_votes = {VOTOS[i]:votes[i] for i in range(len(VOTOS))}
            poll_status = ESTADOS.index("REPROVADO")
            if poll.status != ESTADOS.index("2VOLTA"):
                if final_votes["SIM"] > final_votes["NAO"] + final_votes["ABSTER"]:
                    poll_status = ESTADOS.index("APROVADO")
                elif final_votes["ABSTER"] >= final_votes["NAO"]:
                    poll_status = ESTADOS.index("2VOLTA")
            elif final_votes["SIM"] > final_votes["NAO"]:
                # em segunda volta, abstencoes não contam
                poll_status = ESTADOS.index("APROVADO")

            poll.status = poll_status
            db.session.merge(poll)
            db.session.commit()

            return poll
    
    # não existem votos na proposta
    return None
