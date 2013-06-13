var http = require('http');
var url = require('url');
var sqlite3 = require('sqlite3');
var fs = require('fs');
var S = require('string');

function get_template_folder() {
    return __dirname + "/templates/";
}

function get_database_folder() {
    folder = __dirname + "/../database/";
    console.log("folder: " + folder);
    return folder;
}

function bind_sql_template(response, template, sql, query) {
    var templateFile = get_template_folder() + template;
    console.log("using template: " + templateFile);
    fs.readFile(templateFile, 'utf8', function(err, content) {
        var header = ""; var body = "", footer = "", state = "";
        var i = 0, j;
        while (i < content.length) {
            j = content.indexOf("\n", i);
            if (j == -1)
                j = content.length;
            line = content.substring(i, j);
            if (line.indexOf("{header}") == 0) {
                state = "header";
            } else if (line.indexOf("{body}") == 0) {
                state = "body";
            } else if (line.indexOf("{footer}") == 0) {
                state = "footer";
            } else switch (state) {
                case "header":
                    header += line + "\n";
                    break;
                case "body":
                    body += line + "\n";
                    break;
                case "footer":
                    footer += line + "\n";
                    break;
            };
            i = j + 1;
        }
        bindingDatabase(response, sql, query, header, body, footer);
    });
}

function bindingDatabase(response, sql, query, header, body, footer) {
    var database = get_database_folder() + 'lianhuanhua.db';
    console.log("binding database from: " + database);
    var db = new sqlite3.Database(database);
    var dbSelectStmt = db.prepare(sql);

    // header
    response.writeHead(200, {'Content-Type': 'text/html'});
    // body
    for (key in query) {
        header = S(header).replaceAll("%" + key + "%", query[key]).s;
    }
    response.write(header);

    console.log(dbSelectStmt);
    dbSelectStmt.each(function (err, row) {
        var str = body;
        for (key in row) {
            str = S(str).replaceAll("%" + key + "%", row[key]).s;
        }
        for (key in query) {
            str = S(str).replaceAll("%" + key + "%", query[key]).s;
        }
	    response.write(str);
        }, function () {
            for (key in query) {
                footer = S(footer).replaceAll("%" + key + "%", query[key]).s;
            }
            response.write(footer);
            response.end();
        });
}

function processRequest(request, response) {
    "use strict";
    var pathname, query;
    console.log("\nOn: " + Date());
    console.log("Connection from: " + request.connection.remoteAddress);
    console.log("url: " + request.url)
    pathname = url.parse(request.url).pathname;
    query = url.parse(request.url).query;

    console.log(require('querystring').parse(query));
    console.log('pathname:' + pathname);

    if (pathname === '/') {
        var sqlDirectory = 'SELECT ROWID,* FROM directory ORDER BY catagory, title';
        console.log("response_directory");
        bind_sql_template(response, "directory.html", sqlDirectory, null);
    } else if (pathname === '/content') {
        var sqlContent = 'SELECT ROWID,* FROM content';
        var q = require('querystring').parse(query)
        sqlContent += " WHERE dir_id=" + q['id'] + " ORDER BY page";
        console.log("response_content: " + sqlContent);
        bind_sql_template(response, "content.html", sqlContent, q);
    }
}

var server_port = 8888;
var test_port = 8000;
var port = test_port;

process.argv.forEach(function(val, index) {
    if (val == 'server')
        port = server_port;
});

http.createServer(processRequest).listen(port);
if (port != server_port)
    console.log('using "server" to start port ' + server_port)
console.log('started: ' + port); 
