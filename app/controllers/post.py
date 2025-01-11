from app.models import Post

class PostController:
    def get_post_by_user(user_id: int):
        posts = Post.query.filter_by(user_id=user_id).all()
        return posts
    
    def create_post(title: str, content: str, user_id: int, image: str = None):
        post = Post(
            title=title,
            content=content,
            image=image,
            user_id=user_id,
        )
        post.save()