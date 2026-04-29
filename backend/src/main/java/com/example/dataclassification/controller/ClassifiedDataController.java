package com.example.dataclassification.controller;

import com.example.dataclassification.model.ClassifiedData;
import com.example.dataclassification.service.ClassifiedDataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/classified-data")
public class ClassifiedDataController {

    @Autowired
    private ClassifiedDataService service;

    // ✔ UPDATE (PUT)
    @PutMapping("/{id}")
    public ResponseEntity<?> updateData(@PathVariable Long id, @RequestBody ClassifiedData data) {
        return ResponseEntity.ok(service.update(id, data));
    }

    // ✔ SOFT DELETE
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteData(@PathVariable Long id) {
        service.softDelete(id);
        return ResponseEntity.ok("Deleted successfully");
    }

    // ✔ SEARCH API
    @GetMapping("/search")
    public ResponseEntity<?> search(@RequestParam String q) {
        return ResponseEntity.ok(service.search(q));
    }
}