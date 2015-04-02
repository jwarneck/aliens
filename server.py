import psycopg2
import psycopg2.extras

from flask import Flask, render_template, request
app = Flask(__name__)


def connectToDB():
  #connectionString= 'dbname=music user=postgres password=kirbyk9 host=localhost'
  connectionString = 'dbname=aliens user=postgres password=1967Gt500 host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/')
def mainIndex():
    return render_template('index.html', selectedMenu='Home')

@app.route('/report')
def report():
  return render_template('report.html', selectedMenu='Report')

@app.route('/report2', methods=['POST'])
def report2():
  
  abduction = {'firstname': request.form['firstname'],
               'lastname': request.form['lastname'], 'month': request.form['month'],
               'day': request.form['day'], 'year': request.form['year'],
               'city': request.form['city'], 'state': request.form['state'],
               'scary': request.form['scary'], 'doing': request.form['doing']}
  appearance = request.form.getlist('appearance')
  
  appearance_string = ""
  ship_string= ""
  for value in appearance:
    appearance_string += value + ","
  if len(appearance) > 0:
    appearance_string = appearance_string[: -1]
  
  ship_string = request.form.getlist('ship')[0]
  #print(request.form.getlist('appearance'))
  conn = connectToDB()
  cur = conn.cursor()
  query = 'INSERT INTO abductions (firstname, lastname, city, state, month, day, year, scary, appearance, ship) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
  data = (abduction['firstname'], abduction['lastname'], abduction['city'], abduction['state'], abduction['month'], abduction['day'], abduction['year'], abduction['scary'], appearance_string, ship_string)
  cur.execute(query, data)
  conn.commit()
  
  return render_template('report2.html', abduction = abduction, appearance = appearance, ship=ship_string)

@app.route('/list_abductions')
def abductions():
  
  conn = connectToDB() #psycopg2.connect() "dbname='abductions' user='postgres' password='1967Gt500'")
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  query = 'SELECT * FROM abductions;'
  cur.execute(query)
  results = cur.fetchall()
  for result in results:
    result["appearance"] = result["appearance"].split(",")
  return render_template('list_abductions.html', results=results)

@app.route('/simple')
def simple():
  return render_template('simple.html')

@app.route('/simple2', methods=['POST'])
def simple2():
  return render_template('simple2.html')


@app.route('/simple3')
def simple3():
  return render_template('simple3.html')

@app.route('/simple4', methods=['POST'])
def simple4():
  return render_template('simple4.html', name=request.form['name'])

@app.route('/music')
def showChart():
  """rows returned from postgres are just an ordered list"""
  
  conn = connectToDB()
  cur = conn.cursor()
  try:
    cur.execute("select artist, name from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  return render_template('music.html', albums=results)



@app.route('/music2')
def showChartUsingPythonDictionary():
  """rows returned from postgres are a python dictionary (can
  also be treated as an ordered list)"""
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  try:
    cur.execute("select artist, name from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  print results
  return render_template('music2.html', albums=results)


@app.route('/music3', methods=['GET', 'POST'])
def showChartForms():
  """rows returned from postgres are a python dictionary (can
  also be treated as an ordered list)"""
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  if request.method == 'POST':
    # add new entry into database
    try:
      cur.execute("""INSERT INTO albums (artist, name, rank) 
       VALUES (%s, %s, %s);""",
       (request.form['artist'], request.form['album'], request.form['rank']) )
    except:
      print("ERROR inserting into albums")
      print("Tried: INSERT INTO albums (artist, name, rank) VALUES ('%s', '%s', '%s')") 
      conn.commit()

  try:
    cur.execute("select artist, name from albums")
  except:
    print("Error executing select")
  results = cur.fetchall()
  for r in results:
    print r['artist']
  return render_template('music3.html', albums=results)



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)
