from GustavSelfBot import log

from GustavSelfBot.Events.__on_message__ import func_on_message
from GustavSelfBot.Events.__on_ready__ import func_on_ready
from GustavSelfBot.Events.__on_voice_state_update__ import func_on_voice_state_update

log.info("Events module loaded!")
