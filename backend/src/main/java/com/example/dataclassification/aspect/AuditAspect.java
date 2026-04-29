import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class AuditAspect {

    @After("execution(* com.example.dataclassification.service.*.create*(..)) || " +
           "execution(* com.example.dataclassification.service.*.update*(..)) || " +
           "execution(* com.example.dataclassification.service.*.delete*(..))")
    public void logAudit(JoinPoint joinPoint) {
        String method = joinPoint.getSignature().getName();
        System.out.println("AUDIT LOG: Method executed → " + method);
    }
}