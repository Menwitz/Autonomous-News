from quillbot import quillbot

def main():
    paragraph = (
        '''Different free writing compositions are used to inform various target audiences.
        They can be find in almost any source, which includes print media and online sources. 
        With the advancement of modern technology, such sources have become more easier to access by the day.
        The word article can be used to refer to a brief written composition which is often found
        among other compositions typically included in different publications (e.g. newspaper, magazines, online, etc).
        An article can tackle about different topics, depending on the writer, and is usually intended for a target audience.
        Article writing example is the process of writing an article for a specific purpose and audience. 
        Articles are written to discuss different subjects or topics. Articles included in publications usually 
        contain information on current issues or events happening around the area of the writer or the publication.
        Writers present information in various ways, such as in an informative, or argumentative form. Basis of information 
        written on articles may vary. Such facts may be gathered from different sources, such as eyewitness accounts, 
        one on one interviews, and online, among others.'''
    )

    options = {
        'headless': False,  # default will be True -> TODO
        'language': 'English (AU)',  # default 'English (UK)'
        'mode': 'Fluency',  # default 'Standard'
        'synonymsLevel': 0  # default is 50, can be set from 0 to 100
    }

    paraphrased = quillbot(paragraph, options)

    print('Before:')
    print(paragraph)
    print('\n\nParaphrased:')
    print(paraphrased)

if __name__ == '__main__':
    main()
