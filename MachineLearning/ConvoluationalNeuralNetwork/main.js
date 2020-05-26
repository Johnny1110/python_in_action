var result =[
   {
        'ProjectName' : 'ABC',
         'Name' : '123',
         'Url' : '999'
    }
]

var dataYouWanted = {}

for (var i = 0; i < result.length; ++i){
    dataYouWanted[result[i]['ProjectName'] + result[i]['Name']] = result[i]['Url']
}

console.log(result)
console.log(dataYouWanted)