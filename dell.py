import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


load_dotenv()

GOOGLE_API_KEY = "AIzaSyBGByf31jfvZ3eBZ58lsZuOmwFLqRP1oAU"

st.set_page_config(page_title="Dell AI Support")

st.title("Dell AI Support Bot")

st.write("Ask any Dell laptop issue")

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://www.dell.com/support/home/en-in",
    "Upgrade-Insecure-Requests": "1",
}

URLS = ["https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/software-and-downloads/support-assist/supportassist-for-home",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/blue-screen",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/no-power",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/no-post",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/no-boot",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/bios-uefi",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/system-performance",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/computer-automatic-restart-or-reboot",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/computer-cannot-shutdown",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/common-noises-from-computer",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/computer-cannot-sleep-or-hibernate",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/fix-common-issues/usb-ports-not-working",
"https://www.dell.com/support/kbdoc/en-in/000124295/guide-to-dell-docking-stations",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/docking-stations/setup-dell-docks",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/docking-stations/dell-universal",
"https://www.dell.com/support/kbdoc/en-in/000132851/how-to-troubleshoot-multiple-monitor-issues",
"https://www.dell.com/support/kbdoc/en-in/000202072/how-to-identify-dell-wired-docking-station-diagnostic-indicators",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/docking-stations/dell-rugged",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/docking-stations/dell-thunderbolt",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/audio-and-speakers/connect-dell-soundbar",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/audio-and-speakers/connect-speakers-to-pc",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/audio-and-speakers/connect-headset-headphone",
"https://www.dell.com/support/kbdoc/en-in/000149193/how-do-i-stop-my-computer-s-microphone-from-causing-feedback-through-the-speakers",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/audio-and-speakers/microphone",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/audio-and-speakers/speakers-and-headphones",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wi-fi-network-standards-overview",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/protect-and-secure-home-wifi",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/improve-wifi-speed",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/pair-bluetooth-devices-windows-ubuntu",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/bluetooth",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wired-networking",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/networking-wifi-and-bluetooth/wireless-networking",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/battery-and-power/fan",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/battery-and-power/battery",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/battery-and-power/ac-adapter",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/battery-and-power/no-power",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/mouse-keyboard-touchpad/set-up-your-mouse",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/mouse-keyboard-touchpad/set-up-your-keyboard",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/mouse-keyboard-touchpad/laptop-keyboard-not-working",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/mouse-keyboard-touchpad/touchpad",
"http://dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/mouse-keyboard-touchpad/mouse",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/mouse-keyboard-touchpad/keyboard",
"https://www.dell.com/support/kbdoc/en-in/000336300/dell-digital-delivery-and-alienware-digital-delivery-end-of-life-announcement",
"https://www.dell.com/support/kbdoc/en-in/000201067/dell-display-and-peripheral-manager-for-macos",
"https://www.dell.com/support/kbdoc/en-in/000287285/dell-display-and-peripheral-manager-for-windows",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/connect-monitor-to-computer",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/connect-laptop-to-display",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/setup-dual-triple-monitor",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/guide-daisy-chain-monitors",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/projectors",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/kvm-setup-guide-dell-monitors",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/dell-monitor-firmware-update-guide",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/laptop-display-screen-not-working",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/monitors-and-screens",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/multiple-displays-not-working",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/laptop-touchscreen-not-working",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/monitor-screen-video/webcams",
"https://www.dell.com/support/kbdoc/en-in/000131809/steps-for-updating-the-firmware-for-your-dell-monitor",
"https://www.dell.com/support/kbdoc/en-in/000128638/guide-to-raid-redundant-array-of-independent-disks",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/data-storage-backup-and-recovery/hard-drive-ssd-issues",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/data-strage-backup-and-recovery/support-for-hard-disk-drive",
"https://www.dell.com/support/security/en-in",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/enterprise-resource-center/server-operating-system-support",
"https://www.dell.com/support/kbdoc/en-in/000123958/dell-poweredge-server-start-up-guide",
"https://www.dell.com/support/kbdoc/en-in/000128648/support-articles-for-dell-poweredge-servers",
"https://www.dell.com/support/kbdoc/en-in/000137343/how-to-identify-which-generation-your-dell-poweredge-server-belongs-to",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/printers/inkjet",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/printers/laser",
"https://www.dell.com/support/contents/en-in/article/product-support/self-support-knowledgebase/dell-gaming/dell-visor-faqs",
"https://www.dell.com/support/kbdoc/en-in/000178575/alienware-overclocking",
"https://learn.microsoft.com/en-in/previous-versions/mixed-reality/enthusiast-guide/wmr-setup-faq",
"https://www.dell.com/support/kbdoc/en-in/000175292/troubleshooting-flickering-video-on-dell-gaming-monitors",
"https://www.dell.com/support/kbdoc/en-in/000103410/how-to-use-the-windows-10-game-bar-to-capture-video-from-applications",
"https://www.dell.com/support/kbdoc/en-in/000127708/installing-and-configuring-the-alienware-command-center-software-for-your-alienware-gaming-keyboards-and-mice",
"https://www.dell.com/support/kbdoc/en-in/000124378/installing-drivers-on-your-alienware-system",
"https://www.dell.com/support/kbdoc/en-in/000149321/how-to-update-video-drivers-for-maximum-gaming-performance",
"https://www.dell.com/support/kbdoc/en-in/000123108/maximizing-your-gaming-performance",
"https://www.dell.com/support/kbdoc/en-in/000152785/introduction-to-dell-gaming-pcs"]


def scrape_url(session, url):
    try:
        response = session.get(
            url,
            timeout=30
        )
        response.raise_for_status()
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )
        main_content = soup.find("main")
        if main_content:
            text = main_content.get_text(separator="\n")
        else:
            text = soup.get_text(separator="\n")
        clean_text = " ".join(text.split())
        return clean_text, None
    
    except Exception as e:
        return None, str(e)

@st.cache_resource
def build_vectorstore():
    documents = []
    skipped_urls = []
    session = requests.Session()
    session.headers.update(BROWSER_HEADERS)

    try:
        session.get("https://www.dell.com/support/home/en-in", timeout=30)
    except requests.RequestException:
        pass

    for url in URLS:
        text, error = scrape_url(session, url)
        if not text:
            skipped_urls.append((url, error))
            continue

        doc = Document(
            page_content=text,
            metadata={
                "source": url
            }
        )
        documents.append(doc)

    if not documents:
        return None, skipped_urls

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        return None, skipped_urls

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore, skipped_urls

# k=4 kya hai?
# search_kwargs={"k": 4}
# means:
# “Top 4 most relevant chunks return karo.”

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)

query = st.chat_input("Say something")

if query:
    with st.spinner("Building Dell Knowledge Base..."):
        vectorstore, skipped_urls = build_vectorstore()

    if vectorstore is None:
        st.error("Could not build the Dell Knowledge Base. Please check the source URLs or your internet connection.")
        st.stop()

    if skipped_urls:
        with st.expander(f"Skipped {len(skipped_urls)} pages"):
            for url, error in skipped_urls[:10]:
                st.write(f"{url} - {error}")
            if len(skipped_urls) > 10:
                st.write(f"...and {len(skipped_urls) - 10} more.")

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    sources = "\n".join(
        [
            doc.metadata["source"]
            for doc in docs
        ]
    )

    prompt = f"""
    You are a Dell Support AI assistant.

    Use the provided Dell documentation context to help the user.

    Even if the issue is not an exact match,
    give the closest troubleshooting steps possible.

    CONTEXT:
    {context}

    USER QUESTION:
    {query}

    Provide:
    1. Likely cause
    2. Step-by-step troubleshooting
    3. Important warnings
    4. When to contact Dell support

    Be practical and helpful.
    """
    response = llm.invoke(prompt)
    with st.chat_message("assistant"):
        st.write(response.content)
        st.write("### Sources")
        sources = [doc.metadata["source"] for doc in docs]
        for source in sources:
            st.write(source)
