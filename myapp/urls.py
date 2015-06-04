from django.conf.urls import patterns, include, url 

from blog.views import PostDetailView, PostDeleteView
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.posts_index'),

    url(r'^post/new/', 'blog.views.post_new', name="post_new"),
    url(r'^post/create/', 'blog.views.post_create'),
    url(r'^posts/', 'blog.views.posts_index'),
    url(r'^post/(?P<slug>[-\w]+)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'^post/delete/(?P<slug>[-\w]+)/$', login_required(PostDeleteView.as_view())),
    url(r'^post/edit/(?P<slug>[-\w]+)/$','blog.views.post_edit'),
    url(r'^post/edited/(?P<slug>[-\w]+)/$','blog.views.post_edited'),

    url(r'^comment/create/', 'blog.views.comment_create'),
    url(r'^comment/delete/', 'blog.views.comment_delete'),

    url(r'^tag/new/', 'blog.views.tag_new'),
    url(r'^tag/create/', 'blog.views.tag_create'),

    url(r'^login/', 'blog.views.login_view'),
    url(r'^logout/', 'blog.views.logout_view'),
    url(r'^accounts/auth/', 'blog.views.auth_view')
    )
    # url(r'^myapp/', include('myapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#     url(r'^admin/', include(admin.site.urls)),
# )

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
# ]