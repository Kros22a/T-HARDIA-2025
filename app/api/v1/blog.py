# app/api/v1/routes/blog.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.blog import BlogPost
from datetime import datetime
import re

router = APIRouter()

# ✅ Base de datos local (puedes ampliarla o cargarla desde un JSON)
BLOG_POSTS = [
    {
        "title": "Cómo Armar tu Primera PC",
        "content": "Guía completa para construir tu primera computadora desde cero...",
        "category": "guides",
        "author": "T-Hardia Team",
        "tags": ["pc building", "beginner", "tutorial"]
    },
    {
        "title": "Comparativa de GPUs 2024",
        "content": "Análisis detallado de las mejores tarjetas gráficas del mercado...",
        "category": "reviews",
        "author": "T-Hardia Team",
        "tags": ["gpu", "graphics", "performance"]
    },
    {
        "title": "Optimización de Sistemas Gaming",
        "content": "Consejos para maximizar el rendimiento de tu sistema gaming...",
        "category": "optimization",
        "author": "T-Hardia Team",
        "tags": ["gaming", "optimization", "performance"]
    }
]

def generate_slug(title: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


@router.get("/", response_model=List[BlogPost])
async def get_all_blog_posts():
    """Obtener todos los artículos"""
    posts = []
    for i, post_data in enumerate(BLOG_POSTS):
        post = BlogPost(
            id=str(i + 1),
            title=post_data["title"],
            content=post_data["content"],
            category=post_data["category"],
            author=post_data["author"],
            slug=generate_slug(post_data["title"]),
            created_at=datetime.utcnow(),
            tags=post_data["tags"],
            views=0
        )
        posts.append(post)
    return posts


@router.get("/{slug}", response_model=BlogPost)
async def get_blog_post_by_slug(slug: str):
    """Obtener un artículo por su slug"""
    for i, post_data in enumerate(BLOG_POSTS):
        if generate_slug(post_data["title"]) == slug:
            return BlogPost(
                id=str(i + 1),
                title=post_data["title"],
                content=post_data["content"],
                category=post_data["category"],
                author=post_data["author"],
                slug=slug,
                created_at=datetime.utcnow(),
                tags=post_data["tags"],
                views=0
            )
    raise HTTPException(status_code=404, detail="Artículo no encontrado")


@router.get("/category/{category}", response_model=List[BlogPost])
async def get_blog_posts_by_category(category: str):
    """Filtrar artículos por categoría"""
    posts = [
        BlogPost(
            id=str(i + 1),
            title=p["title"],
            content=p["content"],
            category=p["category"],
            author=p["author"],
            slug=generate_slug(p["title"]),
            created_at=datetime.utcnow(),
            tags=p["tags"],
            views=0
        )
        for i, p in enumerate(BLOG_POSTS) if p["category"].lower() == category.lower()
    ]
    return posts
