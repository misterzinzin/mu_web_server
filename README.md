# mu_web_server
mycro web server for micropython

usage:


        import mu_web_server
        server = mu_web_server.mu_web_server()
        server.start()

        server.globalVar.i = 0

        def pageTest(globalVar,args):
            return '<html><head><meta http-equiv="refresh" content="2"></head><body>test<br>counter = ' + str(server.globalVar.i)+ '</body></html>'
        
        server.pageFunctions['/test'] = pageTest
        
        server.pageFunctions['/'] = pageTest
