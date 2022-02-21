const ArticlesListWithHOC = HOC(ArticlesList, 
        (GlobalDataSource) => GlobalDataSource.getArticles()
    );
const UsersListWithHOC = HOC(UsersList, 
        (GlobalDataSource) => GlobalDataSource.getUsers()
    );