# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 17:24:08 2022

@author: shrey
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)