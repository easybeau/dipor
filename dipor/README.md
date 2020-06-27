# dipor
A Static Site Generator written in Python that bridges the learning curve and helps you gnerate fast and performant static sites


----
settings.py
src/
    content/
        - common.md
        - app1/ (eg. homepage)
            - file1.md (file name should not have spaces, if it has spaces, the context variable will     remove the spaces and have that as variable name)
            - file2.md
            - file3.md
        - app2/ (eg, blog)
            -- file1.md
            -- post1/
            -- post2/
            -- post3/
        - app3/ (eg, profile page for team members)
        - app4/ (extra special glittery unicorn blog posts for vips)

    themes/
        - common.tpl
        - app1/
            [content/app1/*.md context will be vailable
            content/common.md context will be available
            these will be available as
            content
            meta.name
            file1.content
            file2.content
            file3.content
            file1.meta.name, file2.meta.name]
            - main.tpl ( the main html, that either extends or includes other templates )
            - parent.tpl
            - child.tpl
            - there should be ONE main.html
            (if not present, will skip rendering)
        - app2/
        - app3/
        - app4/


- can have multiple file frmats in an app
- will need to specify a reader or can automaticaly detect a reader and do

user needs to
    - have content ready
    - have a theme ready with blocks
    - run build
    - run serve to serve




{'common': 
    {'content': '',
    'meta': 
        {'a': ['this is common']
        }
    },
    
'section2':
    {'content': '<p>welcome to the the club</p>', 
    'meta': 
        {'title': ['related posts']
        }
    },
'section1':
    {'content': '<h1>Decription</h1>\n<p>Amazing Human slash Genius</p>',
    'meta': 
        {'title': ['Wentworth Miller'],
        'show': ['Prison Break']
        }
    }
}


{'common': 
    {'a': ['this is common']
    },
'section2':
    {'title': ['related posts']
    },
'section1':
    {'title': ['Justin Bieber'],
    'show': ['Never Say Never']
    }
}


{'common': 
    {'content': '', 
    'a': ['this is common']
    }, 
'section2': 
    {'content': '<p>welcome to the the club</p>', 
    'title': ['related posts']
    }, 
'section1': 
    {'content': '<h1>Decription</h1>\n<p>Misunderstood, a lot.</p>', 
    'title': ['Justin Bieber'], 
    'show': ['Never Say Never']
    }
}