from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

from genai_test_lib.text_comparision.output_parser import output_res_parser


class TextCompare:
    PROMPT_TEXT = """
            You will be given an expected sentence: {expected_sentence}.
            You will also be provided with an actual sentence: {actual_sentence}.
            Identify and list the keywords present in both the expected and actual sentences.
            If the keywords in the expected sentence do not match those in the actual sentence, decrease the comparison score significantly.
            Similarly, if the numerical values in the expected sentence do not match those in the actual sentence, decrease the comparison score significantly.
            Assign a comparison score between 0 and 10, taking into account the importance of keywords and numerical values.
            Explain the score by providing a reason and listing the keywords that were considered.
            {format_instructions}"""

    def text_compare_promt(self, expected_sentence, actual_sentence):
        text_compare_prompt_template = PromptTemplate(input_variables=["expected_sentence", "actual_sentence"],
                                                      template=TextCompare.PROMPT_TEXT,
                                                      partial_variables={
                                                          "format_instructions": output_res_parser.get_format_instructions()}
                                                      )
        llm = ChatOpenAI(engine="gpt-4")
        chain = LLMChain(llm=llm, prompt=text_compare_prompt_template)
        res = chain.run({"expected_sentence": expected_sentence, 'actual_sentence': actual_sentence})
        return output_res_parser.parse(res).to_dict()


if __name__ == "__main__":
    expected_sentence = '''The number of units sold in the category "Ready to Eat Cereal" is 9.44457% compared to the previous year.'''
    actual_sentence = '''The number of units sold in the category "Ready to Eat Cereal" is 100.44% from the previous year.'''
    res=TextCompare().text_compare_promt(expected_sentence, actual_sentence)
    print(res)
