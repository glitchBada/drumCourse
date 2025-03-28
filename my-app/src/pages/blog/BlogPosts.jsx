import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './BlogPost.scss'

const BlogPosts = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get('http://192.168.43.61:8000/api/posts/');
                setPosts(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching posts:', error);
            }
        };

        fetchPosts();
    }, []);

    if (loading) return <div>Загрузка...</div>;

    return (
        <>
        <div className='blogPage'>
            <h1 className='celebrations'>События нашей школы</h1>
            <div className="blog-container">
                {posts.map(post => (
                    <div key={post.id} className="blog-post">
                        <h2>{post.title}</h2>
                        {post.images && (
                            <img 
                                src={`http://192.168.43.61:8000${post.images}`} 
                                alt={post.title}
                                className="post-image"
                            />
                        )}
                        <p className="post-content">
                            {post.content}
                        </p>
                        <p className="post-date">
                            {new Date(post.pub_date).toLocaleDateString()}
                        </p>
                    </div>
                ))}
            </div>
        </div>
        
        </>
    );
};

export default BlogPosts;