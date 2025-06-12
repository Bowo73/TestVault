package com.example.demo.controller;

import com.example.demo.model.Product;
import com.example.demo.service.ProductService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class ProductController {
    private final ProductService service;

    public ProductController(ProductService service) {
        this.service = service;
    }

    @GetMapping("/products")
    public String listProducts(Model model) {
        model.addAttribute("products", service.findAll());
        model.addAttribute("product", new Product());
        return "products";
    }

    @PostMapping("/products")
    public String createProduct(@ModelAttribute Product product) {
        service.save(product);
        return "redirect:/products";
    }
}
