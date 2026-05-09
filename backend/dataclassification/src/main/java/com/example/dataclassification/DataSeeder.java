package com.example.dataclassification;

import com.example.dataclassification.model.ClassifiedData;
import com.example.dataclassification.repository.ClassifiedDataRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataSeeder implements CommandLineRunner {

    private final ClassifiedDataRepository repository;

    public DataSeeder(ClassifiedDataRepository repository) {
        this.repository = repository;
    }

    @Override
    public void run(String... args) {

        if (repository.count() == 0) {

            for (int i = 1; i <= 15; i++) {

                repository.save(
                        new ClassifiedData(
                                "file" + i + ".pdf",
                                "PDF",
                                i % 2 == 0 ? "Confidential" : "Public",
                                70.0 + i,
                                i % 2 == 0 ? "ACTIVE" : "REVIEW"
                        )
                );
            }

            System.out.println("Demo data inserted!");
        }
    }
}