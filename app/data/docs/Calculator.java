/**
 * 간단한 계산기 클래스
 * 기본적인 사칙연산을 수행합니다.
 */
public class Calculator {
    private double result;
    
    /**
     * 생성자
     */
    public Calculator() {
        this.result = 0.0;
    }
    
    /**
     * 덧셈 연산
     * @param a 첫 번째 숫자
     * @param b 두 번째 숫자
     * @return 계산 결과
     */
    public double add(double a, double b) {
        result = a + b;
        return result;
    }
    
    /**
     * 뺄셈 연산
     * @param a 첫 번째 숫자
     * @param b 두 번째 숫자
     * @return 계산 결과
     */
    public double subtract(double a, double b) {
        result = a - b;
        return result;
    }
    
    /**
     * 곱셈 연산
     * @param a 첫 번째 숫자
     * @param b 두 번째 숫자
     * @return 계산 결과
     */
    public double multiply(double a, double b) {
        result = a * b;
        return result;
    }
    
    /**
     * 나눗셈 연산
     * @param a 첫 번째 숫자
     * @param b 두 번째 숫자
     * @return 계산 결과
     * @throws ArithmeticException 0으로 나누는 경우
     */
    public double divide(double a, double b) {
        if (b == 0) {
            throw new ArithmeticException("0으로 나눌 수 없습니다.");
        }
        result = a / b;
        return result;
    }
    
    /**
     * 현재 결과값 반환
     * @return 현재 결과
     */
    public double getResult() {
        return result;
    }
    
    /**
     * 결과 초기화
     */
    public void clear() {
        result = 0.0;
    }
    
    /**
     * 메인 메서드 - 테스트용
     */
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        
        System.out.println("=== 계산기 테스트 ===");
        System.out.println("10 + 5 = " + calc.add(10, 5));
        System.out.println("10 - 3 = " + calc.subtract(10, 3));
        System.out.println("4 * 6 = " + calc.multiply(4, 6));
        System.out.println("15 / 3 = " + calc.divide(15, 3));
    }
}

