from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful, fact-grounded assistant for answering questions based on internal company data."),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template(
        """Use the following retrieved context to answer the question.
            Context:
            {context}
            
            Question:
            {input}
        """
    )
])