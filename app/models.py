from app import db
from flask_login import UserMixin, current_user # Use only for the a USER model
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login


followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id',db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique=True, index=True)
    password = db.Column(db.String(200))
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    pokemon = db.relationship('Pokemon', backref='trainer', lazy='dynamic')
    followed = db.relationship('User',
                    secondary = followers,
                    primaryjoin=(followers.c.follower_id == id),
                    secondaryjoin=(followers.c.followed_id == id),
                    backref=db.backref('followers',lazy='dynamic'),
                    lazy='dynamic'
                    )
    # We want to check if the user is following someone
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # follow a user
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    # unfollow a user
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()

    # get all the posts from the users I am following
    def followed_posts(self):
        #get posts for all the users I'm following
        followed = Post.query.join(followers, (Post.user_id == followers.c.followed_id)).filter(followers.c.follower_id == self.id)
        #get all my own posts
        self_posts = Post.query.filter_by(user_id=self.id)

        #add those together and then I want to sort then my dates in descending order
        all_posts = followed.union(self_posts).order_by(Post.date_created.desc())
        return all_posts





    def has_caught(self, poke):
        return poke in self.pokemon

    # catch a poke
    def catch(self, poke):
        if not self.has_caught(poke):
            self.pokemon.append(poke)
            db.session.commit()

    # release a poke
    def release(self, poke):
        if self.has_caught(poke):
            self.pokemon.remove(poke)
            db.session.commit()


    def remove_duplicates(self):
        unique_names = set()
        for poke in self.pokemon:
            if poke.name not in unique_names:
                unique_names.add(poke.name)
            else:
                self.release(poke)


    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data["email"]
        self.icon = data['icon']
        self.password = self.hash_password(data['password'])

    #salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    # saves the user to the database
    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit() #save everything in the session to the database
    
    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/bottts/{self.icon}.svg'

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    # SELECT * FROM user WHERE id = ???

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # saves the Post to the database
    def save(self):
        db.session.add(self) # add the Post to the db session
        db.session.commit() #save everything in the session to the database

    def edit(self, new_body):
        self.body=new_body
        self.save()
    
    def __repr__(self):
        return f'<id:{self.id} | Post: {self.body[:15]}>'

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    # ability = db.Column(db.String(50))
    base_xp = db.Column(db.String(50))
    hp = db.Column(db.String(50))
    defense = db.Column(db.String(50))
    attack = db.Column(db.String(50))
    url = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def from_dict(self, pokemon):
        self.name= pokemon['name']
        self.base_xp = pokemon['base_xp']
        self.hp = pokemon["hp"]
        self.defense = pokemon['defense']
        self.attack = pokemon['attack']
        self.url = pokemon['url']
        self.user_id = current_user.id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<id: {self.id} | Pokemon: {self.name}>'



# class AllCaughtPokemon(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


