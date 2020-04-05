![](https://github.com/leviplj/restaurant/workflows/Django%20Test/badge.svg)

## 1 Docker
### 1.1 Build Image
```bash
 docker image build -t restaurant .
 ```

 ### 1.2 Run Container
 ```bash
 docker container run --name restaurant -p 80:8000 --rm restaurant
 ```