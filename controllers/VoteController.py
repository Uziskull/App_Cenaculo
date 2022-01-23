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

# -----------------------------------

class PollOrderingError(PollError):
    def __init__(self):
        super().__init__("Essa ordem de proposta é inválida!")

# ----------------------------------------- #
# Variáveis
# ----------------------------------------- #

# inseridas globalmente, para a pagina de voto saber que votos existem
VOTOS = ["SIM", "NAO", "ABSTER"]

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
    current_vote = get_current_poll()
    if current_vote is None:
        raise VotingPeriodError()

    # verificar se proposta existe
    possible_poll = Poll.query.get(poll_id)
    if possible_poll is None:
        raise PollNotFoundError()

    # verificar se proposta está aberta a votos
    if current_vote.vote_id == poll_id:
        has_previous_votes = possible_poll.vote.count() > 0
        raise VotingClosedError(has_previous_votes)

    # verificar se utilizador já votou
    if already_voted(token, poll_id):
        raise DuplicateVoteError()
    
    db.session.add(Vote(token, poll_id, vote_num))
    db.session.commit()

def already_voted(token: str, poll_id: str):
    uv = Vote.query.filter_by(user_token=token, poll_id=poll_id).first()
    return uv is not None

def get_current_poll():
    return ActivePoll.query.first()

def get_all_polls():
    return Poll.query.order_by(Poll.order).all()

def get_all_polls_and_results():
    # este gatafunho devolve todas as propostas e o seu número de votos positivos/negativos/neutros
    # ordem de votos é a estabelecida em 'VOTOS': sim, não, abster
    return db.Query([
            Poll,
            db.func.count(db.case(
                [((Vote.vote_option == 0), Vote.user_token)],
                else_=db.literal_column("NULL")
            )).label(VOTOS[0].lower()),
            db.func.count(db.case(
                [((Vote.vote_option == 1), Vote.user_token)],
                else_=db.literal_column("NULL")
            )).label(VOTOS[1].lower()),
            db.func.count(db.case(
                [((Vote.vote_option == 2), Vote.user_token)],
                else_=db.literal_column("NULL")
            )).label(VOTOS[2].lower())],
            session=db.session) \
        .join(Vote.poll) \
        .group_by(Poll) \
        .order_by(Poll.order) \
        .all()

# ----------------------------------------- #
# GUI
# ----------------------------------------- #

def create_poll(description: str) -> Poll:
    # adicionar proposta no final da lista
    new_poll = Poll(description)
    db.session.add(new_poll)
    db.session.flush()
    db.session.commit()
    return new_poll

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
    map(lambda p: p.order + (1 if poll_going_up else -1), polls)
    # 3. update all
    for p in polls:
        db.session.merge(p)
    db.session.commit()

def edit_poll(poll_id: str, new_description: str) -> None:
    poll = Poll.query.get(poll_id)
    if poll is None:
        raise PollNotFoundError()
    
    poll.description = new_description
    db.session.merge(poll)
    db.session.commit()

def delete_poll(poll_id: str) -> None:
    poll = Poll.query.get(poll_id)
    if poll is None:
        raise PollNotFoundError()
    
    db.session.delete(poll)
    db.session.commit()
