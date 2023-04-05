package golang

func main() {
	var m map[string]string        // 声明一个hashmap，还不能直接使用，必须使用make来初始化
	m = make(map[string]string)    // 初始化一个map
	m = make(map[string]string, 3) // 初始化一个map并附带一个可选的初始bucket（非准确值，只是有提示意义）

	m := map[string]string{} // 声明并初始化

	m := make(map[string]string) // 使用make来初始化
}
