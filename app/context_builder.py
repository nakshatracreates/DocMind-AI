def build_context(chunks):
    context=""

    for index,chunk in enumerate(chunks):
        context+=f"[Source{index+1}:{chunk['filename']}]\n"
        context+=chunk["text"]
        context+="\n\n"

    return context

