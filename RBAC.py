from flask import Flask, request, render_template_string, abort, redirect, url_for

app = Flask(__name__)

# Sample permissions
permissions = {
    'admin': {'create_post', 'edit_own_post', 'edit_any_post', 'delete_post', 'read_post', 'comment_on_post', 'manage_users'},
    'author': {'create_post', 'edit_own_post', 'read_post', 'comment_on_post'},
    'editor': {'edit_any_post', 'read_post', 'comment_on_post'},
    'reader': {'read_post', 'comment_on_post'}
}

# Sample users
users = {
    'alice': {'role': 'admin'},
    'bob': {'role': 'author'},
    'carol': {'role': 'editor'},
    'dave': {'role': 'reader'}
}

# Sample posts
posts = [
    {'id': 1, 'title': 'Post by Bob', 'content': 'Content of post 1', 'owner': 'bob'},
    {'id': 2, 'title': 'Post by Carol', 'content': 'Content of post 2', 'owner': 'carol'}
]

def get_user():
    username = request.args.get('user')
    return users.get(username, None), username

def can(user_id, action, post_owner_id=None):
    user = users.get(user_id)
    if not user:
        return False
    role = user['role']
    perms = permissions.get(role, set())
    if action == 'edit_post':
        if 'edit_any_post' in perms:
            return True
        if 'edit_own_post' in perms and user_id == post_owner_id:
            return True
        return False
    return action in perms

@app.route('/')
def index():
    user, username = get_user()
    if not user:
        return render_template_string('''
            <h1>Select User</h1>
            <ul>
            {% for name in users %}
                <li><a href="/?user={{name}}">Login as {{name}} ({{users[name].role}})</a></li>
            {% endfor %}
            </ul>
        ''', users=users)

    return render_template_string('''
        <h1>Blog Posts (Logged in as {{username}})</h1>
        <p>Role: {{ users[username].role }}</p>
        {% if can(username, 'create_post') %}
            <p><a href="/create?user={{username}}">Create New Post</a></p>
        {% endif %}
        <ul>
        {% for post in posts %}
            <li>
                <strong>{{post.title}}</strong> by {{post.owner}}<br>
                {{ post.content }}<br>
                {% if can(username, 'edit_post', post.owner) %}
                    <a href="/edit/{{post.id}}?user={{username}}">Edit</a>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
        <hr>
        <h3>Switch User</h3>
        <ul>
        {% for name in users %}
            <li><a href="/?user={{name}}">Switch to {{name}} ({{users[name].role}})</a></li>
        {% endfor %}
        </ul>
    ''', posts=posts, can=can, username=username, users=users)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    user, username = get_user()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        abort(404)
    if not can(username, 'edit_post', post['owner']):
        abort(403)

    if request.method == 'POST':
        post['content'] = request.form['content']
        return redirect(url_for('index', user=username))

    return render_template_string('''
        <h2>Editing: {{ post.title }}</h2>
        <form method="post">
            <textarea name="content" rows="10" cols="50">{{ post.content }}</textarea><br>
            <button type="submit">Save</button>
        </form>
        <a href="/?user={{username}}">Back to posts</a>
    ''', post=post, username=username)

@app.route('/create', methods=['GET', 'POST'])
def create():
    user, username = get_user()
    if not can(username, 'create_post'):
        abort(403)

    if request.method == 'POST':
        new_id = max(p['id'] for p in posts) + 1 if posts else 1
        new_post = {
            'id': new_id,
            'title': request.form['title'],
            'content': request.form['content'],
            'owner': username
        }
        posts.append(new_post)
        return redirect(url_for('index', user=username))

    return render_template_string('''
        <h2>Create New Post</h2>
        <form method="post">
            Title: <input type="text" name="title"><br>
            <textarea name="content" rows="10" cols="50"></textarea><br>
            <button type="submit">Create</button>
        </form>
        <a href="/?user={{username}}">Back to posts</a>
    ''', username=username)

if __name__ == '__main__':
    print("Pagina HTML simples no endereço local indicado Acima com as funcionalidades demonstradas")
    app.run(debug=True)
