"""
=========================================================
📚 模块: 22 异步 IO（AI Agent 的核心）
💡 核心对比：
1. asyncio：单线程事件循环，遇到 await 挂起并让出 CPU，I/O 就绪后恢复（不同于 Java 多线程阻塞）。
2. asyncio.gather：并发等待多个协程，总耗时约为耗时最长的那一个（而不是相加）。
=========================================================
"""
import asyncio

print("--- 1. 协程与 await 挂起 ---")
async def fetch(url):
    # 任务 1：打印开始抓取，使用 await asyncio.sleep(1) 模拟网络延迟，打印抓取完成。
    # pass
    print(f"开始抓取 {url}...")
    # 这行代码相当于 Java 的 Thread.sleep(1000)，但它不会阻塞整个线程，而是把控制权交还给事件循环
    await asyncio.sleep(1)
    print(f"{url} 抓取完成！")
    return url


print("\n--- 2. 事件循环并发 gather ---")
# 任务 2：用 asyncio.run() 运行单个 fetch。
print("【任务 2：单个 fetch 运行】")
asyncio.run(fetch("A"))
# 任务 3：用 asyncio.gather(fetch('A'), fetch('B'), fetch('C')) 并发执行，打印总耗时。
async def run_concurrent():
    print("\n【任务 3：并发 gather 运行】")
    start_time = time.time()
    # gather 会同时把 A、B、C 三个任务放进事件循环中，遇到 sleep 立刻切换
    await asyncio.gather(fetch("A"), fetch("B"), fetch("C"))
    end_time = time.time()
    print(f"并发总耗时: {end_time - start_time:.2f} 秒")
# 任务 4：对比串行执行 3 次 await fetch() 的耗时差异。
async def run_sequential():
    print("\n【任务 4：串行运行】")
    start_time = time.time()
    # 老老实实排队：等 A 完成了，再等 B，再等 C
    await fetch("A")
    await fetch("B")
    await fetch("C")
    end_time = time.time()
    print(f"串行总耗时: {end_time - start_time:.2f} 秒")



print("\n--- 3. 异步超时与取消机制 ---")
# 任务 5：使用 asyncio.wait_for() 为耗时任务设置 0.5 秒超时，观察 TimeoutError。

async def run_timeout():
    print("\n【任务 5：超时测试】")
    try:
        # fetch 需要 1 秒，但我们只给它 0.5 秒的时间
        await asyncio.wait_for(fetch("D"), timeout=0.5)
    except asyncio.TimeoutError:
        print("❌ 抓取超时啦！(TimeoutError)")


if __name__ == "__main__":
    # 依次运行这些异步测试
    asyncio.run(run_concurrent())
    asyncio.run(run_sequential())
    asyncio.run(run_timeout())