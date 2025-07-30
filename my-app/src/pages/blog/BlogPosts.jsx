import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './BlogPost.scss'

const BlogPosts = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get('http://194.87.76.29:8000/api/posts/');
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
            <h1 className='celebrations'>События <span>нашей школы</span></h1>
            <div className="blog-container">
                {posts.map(post => (
                    <div key={post.id} className="blog-post">
                        <div className='postTitle' dangerouslySetInnerHTML={{ __html: post.title }}/>
                        <div className='imgandcontent'>
                            {post.images && (
                                <img 
                                    src={`http://194.87.76.29:8000/${post.images}`} 
                                    alt={post.title}
                                    className="post-image"
                                />
                            )}
                            {/* <p className="post-content">
                                {post.content}
                            </p> */}
                            <div
                                className="post-content"
                                dangerouslySetInnerHTML={{ __html: post.content }}
                            />                        
                        </div>
                        
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