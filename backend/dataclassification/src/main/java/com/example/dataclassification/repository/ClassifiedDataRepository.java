package com.example.dataclassification.repository;

import com.example.dataclassification.model.ClassifiedData;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ClassifiedDataRepository
        extends JpaRepository<ClassifiedData, Long> {
}