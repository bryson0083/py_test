"""

Ref:
	https://medium.com/@andy.lane/convert-pandas-dataframes-to-images-using-imgkit-5da7e5108d55

"""
import pandas
import imagekit

data = pandas.read_csv(open("biostats.csv", "r"))

# modified from http://cssmenumaker.com/br/blog/stylish-css-tables-tutorial
css = """
<style type=\"text/css\">
table {
color: #333;
font-family: Helvetica, Arial, sans-serif;
width: 640px;
border-collapse:
collapse; 
border-spacing: 0;
}

td, th {
border: 1px solid transparent; /* No more visible border */
height: 30px;
}
th {
background: #DFDFDF; /* Darken header a bit */
font-weight: bold;
}
td {
background: #FAFAFA;
text-align: center;
}
table tr:nth-child(odd) td{
background-color: white;
}
</style>
"""

text_file = open("filename.html", "a")
# write the CSS
text_file.write(css)
# write the HTML-ized Pandas DataFrame
text_file.write(data.to_html())
text_file.close()

# imagekit.from_file編譯錯誤
imgkitoptions = {"format": "png"}
#imagekit.from_file("filename.html", outputfile, options=imgkitoptions)