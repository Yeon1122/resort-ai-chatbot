# pdf2html.py
import os
import warnings
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_upstage import UpstageDocumentParseLoader



warnings.filterwarnings("ignore")

# .env 로드
load_dotenv()
upstage_key = os.getenv("UPSTAGE_API_KEY")


# pdf파일을 html로 data load 과정.
def parse_pdf_to_html(pdf_path, output_html_path):
    # PDF 파싱: HTML로
    loader = UpstageDocumentParseLoader(
        pdf_path,
        output_format='html',
        coordinates=False
    )
    #36페이지가 1덩어리로 로드.
    docs = loader.load()
    html_content = docs[0].page_content
     
    # 전체 HTML 저장
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"전체 HTML 저장: {output_html_path}")

    return html_content


if __name__ == "__main__":
    # 올바른 상대경로 지정
    input_pdf = "./input/재활용품 분리배출 가이드라인(2018).pdf"
    output_html = "./output/parsed_output.html"

    pages = parse_pdf_to_html(input_pdf, output_html)