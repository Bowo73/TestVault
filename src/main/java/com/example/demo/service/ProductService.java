package com.example.demo.service;

import com.example.demo.model.Product;
import com.example.demo.repository.ProductRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProductService {
    private final ProductRepository repo;

    public ProductService(ProductRepository repo) {
        this.repo = repo;
    }

    public List<Product> findAll() { return repo.findAll(); }
    public Product save(Product p) { return repo.save(p); }
    public Product update(Long id, Product p) {
        p.setId(id);
        return repo.save(p);
    }
    public void delete(Long id) { repo.deleteById(id); }
}
