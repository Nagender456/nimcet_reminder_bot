from telethon.tl.types import InputMediaPoll, Poll, PollAnswer
import random

def create_poll(correct_option: str = None):
	options_poll = InputMediaPoll(
		poll = Poll(
			id = random.randint(1, 10**10),
			question = '.',
			answers = [
				PollAnswer('A', bytes('a', 'utf-8')),
				PollAnswer('B', bytes('b', 'utf-8')),
				PollAnswer('C', bytes('c', 'utf-8')),
				PollAnswer('D', bytes('d', 'utf-8'))
			],
			public_voters = True,
			quiz = correct_option is not None
		)
	)
	if correct_option is not None:
		options_poll.correct_answers = [bytes(correct_option, 'utf-8')]

	return options_poll