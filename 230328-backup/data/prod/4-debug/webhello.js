// fetch port from command or fallback
const 
	port = (process.argv[2] || process.env.PORT || 9001),
	http = require('http')

http.createServer((req, res) => {
	// abort favicon.ico request
	if (req.url.includes('favicon.ico')) {
		res.statusCode - 404
		res.end('Not found')
		return
	}


	console.log(req.url)

	const nameArg = capitalize( req.url.replace(/[^\w.,-]/g, ' ').replace(/\s+/g, ' ').trim() || 'world' )

	res.statusCode = 200
	res.setHeader('Content-Type', 'text/html')
	res.end(`<h1>Hello ${ nameArg }!</h1>`)
	
}).listen(port)

console.log(`Server running at http://localhost:${ port }/`)

// capitalize the first letter of all words
function capitalize(str) {
	return str
		.trim()
		.toLowerCase()
		.split(' ')
		.map(word => word.charAt(0).toUpperCase() + word.slice(1))
		.join(' ')
}
