import React, { useState, useEffect } from 'react';
import DOMPurify from 'dompurify';
import api from '../../api/axios';
import './BlogPost.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://194.87.76.29:8000';

const BlogPosts = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/api/posts/')
            .then((res) => setPosts(res.data))
            .catch((err) => console.error('Error fetching posts:', err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div>Загрузка...</div>;

    return (
        <div className='blogPage'>
            <h1 className='celebrations'>События <span>нашей школы</span></h1>
            <div className="blog-container">
                {posts.map((post) => (
                    <div key={post.id} className="blog-post">
                        <div
                            className='postTitle'
                            dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(post.title) }}
                        />
                        <div className='imgandcontent'>
                            {post.images && (
                                <img
                                    src={`${API_URL}/${post.images}`}
                                    alt={post.title}
                                    className="post-image"
                                />
                            )}
                            <div
                                className="post-content"
                                dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(post.content) }}
                            />
                        </div>
                        <p className="post-date">
                            {new Date(post.pub_date).toLocaleDateString('ru-RU')}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BlogPosts;
