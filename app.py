from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

# Create the database and the Item table
with app.app_context():
    db.create_all()

# HTML template with enhanced design and CSS
template = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Flask CRUD App</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .container {
      width: 80%;
      max-width: 600px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      padding: 20px;
      box-sizing: border-box;
    }
    h1 {
      color: #333;
      text-align: center;
    }
    form {
      margin-bottom: 20px;
      display: flex;
      justify-content: center;
    }
    input[type="text"] {
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 4px;
      margin-right: 10px;
      flex: 1;
    }
    input[type="submit"] {
      padding: 10px 20px;
      border: none;
      border-radius: 4px;
      background-color: #007bff;
      color: white;
      cursor: pointer;
    }
    input[type="submit"]:hover {
      background-color: #0056b3;
    }
    ul {
      list-style-type: none;
      padding: 0;
    }
    li {
      padding: 10px;
      border-bottom: 1px solid #ddd;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    a {
      color: #007bff;
      text-decoration: none;
      margin-left: 10px;
    }
    a:hover {
      text-decoration: underline;
    }
    .edit-form {
      margin-top: 20px;
    }
    .edit-form input[type="text"] {
      margin-right: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Item List</h1>
    <form action="/add" method="post">
      <input type="text" name="item" placeholder="New item" required>
      <input type="submit" value="Add">
    </form>
    <ul>
      {% for item in items %}
        <li>
          {{ item.name }}
          <div>
            <a href="{{ url_for('edit', item_id=item.id) }}">Edit</a>
            <a href="{{ url_for('delete', item_id=item.id) }}">Delete</a>
          </div>
        </li>
      {% endfor %}
    </ul>
    {% if edit_item %}
      <div class="edit-form">
        <h2>Edit Item</h2>
        <form action="/update/{{ edit_item.id }}" method="post">
          <input type="text" name="item" value="{{ edit_item.name }}" required>
          <input type="submit" value="Update">
        </form>
      </div>
    {% endif %}
  </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Retrieve all items from the database
    items = Item.query.all()
    return render_template_string(template, items=items, edit_item=None)

@app.route('/add', methods=['POST'])
def add():
    # Get item from form and add to the database
    item_name = request.form.get('item')
    new_item = Item(name=item_name)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:item_id>')
def edit(item_id):
    # Retrieve the item to edit from the database
    item = Item.query.get_or_404(item_id)
    items = Item.query.all()  # Get all items for the list
    return render_template_string(template, items=items, edit_item=item)

@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    # Update the item in the database
    item_name = request.form.get('item')
    item = Item.query.get_or_404(item_id)
    item.name = item_name
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete(item_id):
    # Delete the item from the database
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
