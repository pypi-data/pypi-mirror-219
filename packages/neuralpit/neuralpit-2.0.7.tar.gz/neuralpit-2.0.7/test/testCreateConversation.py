from neuralpit import NeuralPitSDK
from neuralpit.services.conversation import ConversationService
import os

def main():
   NeuralPitSDK.init(os.environ['API_ENDPOINT'],os.environ['API_KEY'])
   service =  ConversationService()
   conversation = {'user_id':'platform@neuralpit.com','id':'CHAT_WITH_DOCUMENTS'}
   conversationId = service.createConversation(conversation)

if __name__ == "__main__":
    main()
